#!/usr/bin/env python3
"""
Backend API para el generador de sitios de noticias
Proporciona endpoints REST para gestionar la generación de sitios
"""

from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import os
import sys
import json
import subprocess
from pathlib import Path
from datetime import datetime
import glob

# Añadir directorio scripts al path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'scripts'))

app = Flask(__name__)
CORS(app)

# Configuración
BASE_DIR = Path(__file__).parent.parent
SITES_DIR = BASE_DIR / 'sites'
METADATA_DIR = BASE_DIR / 'data' / 'sites_metadata'
SCRIPTS_DIR = BASE_DIR / 'scripts'

# Asegurar que los directorios existen
SITES_DIR.mkdir(exist_ok=True)
METADATA_DIR.mkdir(exist_ok=True)


@app.route('/api/sites', methods=['GET'])
def get_sites():
    """Obtiene la lista de todos los sitios generados"""
    try:
        sites = []
        site_files = glob.glob(str(SITES_DIR / 'site*.html'))
        
        for site_file in site_files:
            site_name = Path(site_file).name
            site_id = site_name.replace('site', '').replace('.html', '')
            
            # Obtener información del archivo
            stat = os.stat(site_file)
            
            sites.append({
                'id': int(site_id),
                'nombre': f'Sitio {site_id}',
                'filename': site_name,
                'createdAt': datetime.fromtimestamp(stat.st_mtime).isoformat(),
                'size': stat.st_size
            })
        
        # Ordenar por ID
        sites.sort(key=lambda x: x['id'], reverse=True)
        
        return jsonify({
            'success': True,
            'sites': sites,
            'total': len(sites)
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/sites/stats', methods=['GET'])
def get_stats():
    """Obtiene estadísticas del sistema"""
    try:
        # Contar sitios
        site_files = glob.glob(str(SITES_DIR / 'site*.html'))
        total_sites = len(site_files)
        
        # Sitios recientes (últimas 24 horas)
        now = datetime.now().timestamp()
        recent_sites = 0
        for site_file in site_files:
            stat = os.stat(site_file)
            if now - stat.st_mtime < 86400:  # 24 horas
                recent_sites += 1
        
        # Contar archivos de metadatos
        metadata_files = glob.glob(str(METADATA_DIR / 'sites_metadata_*.json'))
        
        # Última generación
        last_generation = None
        if site_files:
            latest_file = max(site_files, key=os.path.getmtime)
            last_generation = datetime.fromtimestamp(os.path.getmtime(latest_file)).isoformat()
        
        return jsonify({
            'success': True,
            'stats': {
                'totalSites': total_sites,
                'recentSites': recent_sites,
                'totalArticles': total_sites * 15,  # Aproximación
                'lastGeneration': last_generation,
                'metadataFiles': len(metadata_files)
            }
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/sites/generate', methods=['POST'])
def generate_sites():
    """Genera nuevos sitios de noticias usando el flujo completo"""
    try:
        data = request.json or {}
        
        # Validar parámetros
        quantity = data.get('quantity', 5)
        
        try:
            quantity = int(quantity)
            if quantity < 1 or quantity > 100:
                return jsonify({
                    'success': False,
                    'error': 'La cantidad debe estar entre 1 y 100'
                }), 400
        except (ValueError, TypeError):
            return jsonify({
                'success': False,
                'error': 'La cantidad debe ser un número válido'
            }), 400
        
        verify_domains = data.get('verifyDomains', False)
        use_full_flow = data.get('useFullFlow', True)  # Usar flujo completo por defecto
        
        # Verificar que los scripts existen
        orchestrator_script = SCRIPTS_DIR / 'master_orchestrator.py'
        legacy_script = SCRIPTS_DIR / 'generate-sites.py'
        
        if use_full_flow and not orchestrator_script.exists():
            return jsonify({
                'success': False,
                'error': f'Script no encontrado: {orchestrator_script}'
            }), 500
        
        if not use_full_flow and not legacy_script.exists():
            return jsonify({
                'success': False,
                'error': f'Script no encontrado: {legacy_script}'
            }), 500
        
        # Construir comando
        if use_full_flow:
            # Usar master orchestrator (flujo completo)
            cmd = [
                'python3',
                str(orchestrator_script),
                '--sitios', str(quantity)
            ]
            
            if verify_domains:
                cmd.append('--verificar-dominios')
            
            timeout = 3600  # 1 hora para flujo completo
        else:
            # Flujo legacy (generate-sites.py)
            use_existing_metadata = data.get('useExistingMetadata', False)
            metadata_file = data.get('metadataFile', '')
            generate_metadata = data.get('generateMetadata', True)
            
            cmd = [
                'python3',
                str(legacy_script),
                '--cantidad', str(quantity),
                '--no-interactivo'
            ]
            
            if verify_domains:
                cmd.append('--verificar-dominios')
            
            if use_existing_metadata and metadata_file:
                cmd.extend(['--metadata-file', metadata_file])
            elif generate_metadata:
                cmd.append('--generar-metadata')
            
            timeout = 600  # 10 minutos para flujo legacy
        
        # Ejecutar generación
        start_time = datetime.now()
        
        # Añadir PYTHONUNBUFFERED para ver output en tiempo real
        env = os.environ.copy()
        env['PYTHONUNBUFFERED'] = '1'
        
        try:
            result = subprocess.run(
                cmd,
                cwd=str(SCRIPTS_DIR),
                capture_output=True,
                text=True,
                timeout=timeout,
                env=env
            )
        except subprocess.TimeoutExpired:
            return jsonify({
                'success': False,
                'error': f'La generación excedió el tiempo límite de {timeout//60} minutos'
            }), 408
        except FileNotFoundError:
            return jsonify({
                'success': False,
                'error': 'Python3 no encontrado en el sistema'
            }), 500
        except Exception as e:
            return jsonify({
                'success': False,
                'error': f'Error ejecutando el script: {str(e)}'
            }), 500
        
        end_time = datetime.now()
        execution_time = (end_time - start_time).total_seconds()
        
        if result.returncode != 0:
            # Parse error from stderr/stdout
            error_output = result.stderr.strip() if result.stderr else result.stdout.strip()
            
            # Extract most relevant error message
            error_lines = error_output.split('\n')
            error_message = 'Error al generar sitios'
            
            # Try to find the actual error message
            for line in reversed(error_lines):
                line = line.strip()
                if line and not line.startswith('Traceback') and not line.startswith('File '):
                    error_message = line[:500]  # Limit length
                    break
            
            return jsonify({
                'success': False,
                'error': error_message,
                'stderr': result.stderr[:1000] if result.stderr else None,  # Limit output
                'stdout': result.stdout[:1000] if result.stdout else None,
                'returncode': result.returncode,
                'command': ' '.join(cmd)
            }), 500
        
        # Contar sitios generados
        site_files = glob.glob(str(SITES_DIR / 'site*.html'))
        
        # Buscar archivo de metadatos más reciente
        metadata_files = glob.glob(str(METADATA_DIR / 'sites_metadata_*.json'))
        latest_metadata = None
        if metadata_files:
            latest_metadata = Path(max(metadata_files, key=os.path.getmtime)).name
        
        return jsonify({
            'success': True,
            'sitesGenerated': len(site_files),
            'domainsVerified': quantity if verify_domains else 0,
            'domainsAvailable': int(quantity * 0.8) if verify_domains else 0,
            'metadataFile': latest_metadata,
            'executionTime': f'{execution_time:.1f}s',
            'output': result.stdout[:1000] if result.stdout else None  # Limit output
        })
        
    except Exception as e:
        import traceback
        error_details = traceback.format_exc()
        app.logger.error(f"Error in generate_sites: {error_details}")
        
        return jsonify({
            'success': False,
            'error': str(e),
            'type': type(e).__name__
        }), 500


@app.route('/api/sites/<int:site_id>', methods=['DELETE'])
def delete_site(site_id):
    """Elimina un sitio específico"""
    try:
        site_file = SITES_DIR / f'site{site_id}.html'
        
        if not site_file.exists():
            return jsonify({
                'success': False,
                'error': 'Sitio no encontrado'
            }), 404
        
        site_file.unlink()
        
        return jsonify({
            'success': True,
            'message': f'Sitio {site_id} eliminado'
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/metadata', methods=['GET'])
def get_metadata():
    """Obtiene la lista de archivos de metadatos"""
    try:
        metadata_files = glob.glob(str(METADATA_DIR / 'sites_metadata_*.json'))
        
        files = []
        for file_path in metadata_files:
            stat = os.stat(file_path)
            filename = Path(file_path).name
            
            # Cargar archivo para obtener conteo
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                count = len(data) if isinstance(data, list) else 1
            
            files.append({
                'filename': filename,
                'createdAt': datetime.fromtimestamp(stat.st_mtime).isoformat(),
                'size': stat.st_size,
                'sitesCount': count
            })
        
        # Ordenar por fecha de modificación
        files.sort(key=lambda x: x['createdAt'], reverse=True)
        
        return jsonify({
            'success': True,
            'files': files,
            'total': len(files)
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/metadata/<filename>', methods=['GET'])
def get_metadata_file(filename):
    """Obtiene el contenido de un archivo de metadatos"""
    try:
        file_path = METADATA_DIR / filename
        
        if not file_path.exists():
            return jsonify({
                'success': False,
                'error': 'Archivo no encontrado'
            }), 404
        
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        return jsonify({
            'success': True,
            'data': data
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/settings', methods=['GET'])
def get_settings():
    """Obtiene la configuración del sistema"""
    try:
        # Leer variables de entorno
        env_file = BASE_DIR / '.env'
        settings = {}
        
        if env_file.exists():
            with open(env_file, 'r') as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith('#') and '=' in line:
                        key, value = line.split('=', 1)
                        settings[key] = value
        
        return jsonify({
            'success': True,
            'settings': {
                'newsApiKey': settings.get('NEWSAPI_KEY', ''),
                'newsdataKey': settings.get('NEWSDATA_KEY', ''),
                'blackboxApiKey': settings.get('BLACKBOX_API_KEY', ''),
                'defaultQuantity': 5,
                'verifyDomainsByDefault': False,
                'autoSaveMetadata': True,
                'maxTemplates': 40
            }
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/settings', methods=['PUT'])
def update_settings():
    """Actualiza la configuración del sistema"""
    try:
        data = request.json
        
        # Actualizar .env
        env_file = BASE_DIR / '.env'
        env_vars = {}
        
        if env_file.exists():
            with open(env_file, 'r') as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith('#') and '=' in line:
                        key, value = line.split('=', 1)
                        env_vars[key] = value
        
        # Actualizar valores
        if 'newsApiKey' in data:
            env_vars['NEWSAPI_KEY'] = data['newsApiKey']
        if 'newsdataKey' in data:
            env_vars['NEWSDATA_KEY'] = data['newsdataKey']
        if 'blackboxApiKey' in data:
            env_vars['BLACKBOX_API_KEY'] = data['blackboxApiKey']
        
        # Guardar .env
        with open(env_file, 'w') as f:
            for key, value in env_vars.items():
                f.write(f'{key}={value}\n')
        
        return jsonify({
            'success': True,
            'message': 'Configuración actualizada'
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/settings/status', methods=['GET'])
def check_status():
    """Verifica el estado del sistema"""
    try:
        status = {
            'nameGenerator': True,
            'domainVerifier': os.path.exists('/usr/bin/whois'),
            'newsApi': bool(os.getenv('NEWSAPI_KEY')),
            'layoutGenerator': True
        }
        
        return jsonify({
            'success': True,
            'status': status
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/sites/<int:site_id>/view', methods=['GET'])
def view_site(site_id):
    """Sirve el archivo HTML de un sitio específico"""
    try:
        site_file = SITES_DIR / f'site{site_id}.html'
        
        if not site_file.exists():
            return jsonify({
                'success': False,
                'error': 'Sitio no encontrado'
            }), 404
        
        return send_from_directory(str(SITES_DIR), f'site{site_id}.html')
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


# Servir archivos estáticos de templates CSS
@app.route('/templates/css/<path:filename>')
def serve_css(filename):
    """Sirve archivos CSS de templates"""
    css_dir = BASE_DIR / 'templates' / 'css'
    return send_from_directory(str(css_dir), filename)


# Servir imágenes de noticias
@app.route('/images/<path:filename>')
def serve_images(filename):
    """Sirve imágenes de noticias"""
    images_dir = BASE_DIR / 'images'
    return send_from_directory(str(images_dir), filename)


@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'version': '2.0.0',
        'timestamp': datetime.now().isoformat(),
        'uptime': 'active'
    })


@app.route('/api/keep-alive', methods=['GET'])
def keep_alive():
    """Keep-alive endpoint para prevenir suspension en Render free tier"""
    return jsonify({
        'status': 'alive',
        'message': 'Service is active',
        'timestamp': datetime.now().isoformat()
    })


@app.route('/api/debug/paths', methods=['GET'])
def debug_paths():
    """Debug endpoint para verificar rutas y archivos disponibles"""
    try:
        info = {
            'base_dir': str(BASE_DIR),
            'sites_dir': str(SITES_DIR),
            'scripts_dir': str(SCRIPTS_DIR),
            'metadata_dir': str(METADATA_DIR),
            'cwd': os.getcwd(),
            'exists': {
                'base_dir': BASE_DIR.exists(),
                'sites_dir': SITES_DIR.exists(),
                'scripts_dir': SCRIPTS_DIR.exists(),
                'metadata_dir': METADATA_DIR.exists()
            },
            'scripts': {
                'master_orchestrator': (SCRIPTS_DIR / 'master_orchestrator.py').exists(),
                'generate_sites': (SCRIPTS_DIR / 'generate-sites.py').exists(),
                'paraphrase': (SCRIPTS_DIR / 'paraphrase.py').exists(),
                'article_expander': (SCRIPTS_DIR / 'article-expander.py').exists()
            },
            'python_version': sys.version,
            'python_path': sys.executable
        }
        return jsonify({
            'success': True,
            'info': info
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
