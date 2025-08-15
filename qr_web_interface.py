#!/usr/bin/env python3
"""
QR Web Interface - Uses your proven qr_phone_control_loop.py to generate real QR codes
"""

import json
import subprocess
import os
import base64
from pathlib import Path
from http.server import HTTPServer, BaseHTTPRequestHandler
import urllib.parse
import threading
import webbrowser
import time

class QRWebHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            self.serve_html()
        elif self.path.startswith('/generate_qr'):
            self.handle_generate_qr()
        else:
            self.send_error(404)
    
    def do_POST(self):
        if self.path == '/generate_qr':
            self.handle_generate_qr()
        else:
            self.send_error(404)
    
    def serve_html(self):
        html_content = '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>QR Device Control Builder - Real QR Codes</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
            min-height: 100vh;
            color: #333;
        }
        .header {
            background: rgba(255, 255, 255, 0.1);
            backdrop-filter: blur(20px);
            padding: 1.5rem 2rem;
            border-bottom: 1px solid rgba(255, 255, 255, 0.2);
        }
        .header h1 {
            color: white;
            font-size: 2.2rem;
            font-weight: 700;
            margin-bottom: 0.5rem;
        }
        .header p {
            color: rgba(255, 255, 255, 0.8);
            font-size: 1.1rem;
        }
        .container {
            display: grid;
            grid-template-columns: 320px 1fr 400px;
            gap: 2rem;
            padding: 2rem;
            max-width: 1600px;
            margin: 0 auto;
            height: calc(100vh - 140px);
        }
        .panel {
            background: rgba(255, 255, 255, 0.95);
            border-radius: 20px;
            padding: 2rem;
            box-shadow: 0 20px 40px rgba(0, 0, 0, 0.1);
            backdrop-filter: blur(10px);
            border: 1px solid rgba(255, 255, 255, 0.3);
        }
        .panel h3 {
            font-size: 1.4rem;
            margin-bottom: 1.5rem;
            color: #2c3e50;
            font-weight: 600;
        }
        .action-item {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 1rem 1.2rem;
            margin-bottom: 0.8rem;
            border-radius: 12px;
            cursor: pointer;
            border: none;
            width: 100%;
            text-align: left;
            font-size: 0.95rem;
            font-weight: 500;
            display: flex;
            align-items: center;
            gap: 0.8rem;
        }
        .action-item:hover {
            transform: translateY(-3px);
            box-shadow: 0 8px 25px rgba(102, 126, 234, 0.4);
        }
        .workflow-builder {
            background: #f8f9fa;
            border-radius: 16px;
            padding: 2rem;
            min-height: 500px;
            border: 3px dashed #dee2e6;
            overflow-y: auto;
        }
        .workflow-step {
            background: white;
            border-radius: 12px;
            padding: 1.5rem;
            margin-bottom: 1.5rem;
            box-shadow: 0 4px 15px rgba(0, 0, 0, 0.08);
            border-left: 5px solid #667eea;
            position: relative;
        }
        .step-number {
            position: absolute;
            top: -10px;
            left: -10px;
            background: #667eea;
            color: white;
            width: 30px;
            height: 30px;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 0.9rem;
            font-weight: 700;
        }
        .form-group {
            margin-bottom: 1rem;
        }
        .form-group label {
            display: block;
            margin-bottom: 0.5rem;
            font-weight: 600;
            color: #34495e;
            font-size: 0.9rem;
        }
        .form-group input, .form-group textarea {
            width: 100%;
            padding: 0.8rem;
            border: 2px solid #e9ecef;
            border-radius: 8px;
            font-family: inherit;
            font-size: 0.9rem;
        }
        .remove-btn {
            position: absolute;
            top: 1rem;
            right: 1rem;
            background: #e74c3c;
            color: white;
            border: none;
            border-radius: 50%;
            width: 30px;
            height: 30px;
            cursor: pointer;
            font-size: 1rem;
            font-weight: 700;
        }
        .generate-btn {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border: none;
            padding: 1.2rem 2rem;
            border-radius: 12px;
            font-size: 1.1rem;
            font-weight: 600;
            cursor: pointer;
            width: 100%;
            margin-bottom: 2rem;
        }
        .qr-item {
            background: white;
            border-radius: 12px;
            padding: 1.5rem;
            margin-bottom: 1.5rem;
            box-shadow: 0 4px 15px rgba(0, 0, 0, 0.08);
            border: 1px solid #e9ecef;
            text-align: center;
        }
        .qr-item h4 {
            margin-bottom: 1rem;
            color: #2c3e50;
            font-size: 1rem;
        }
        .qr-image {
            margin: 1rem 0;
            border-radius: 8px;
            box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
            max-width: 100%;
        }
        .download-btn {
            background: #27ae60;
            color: white;
            border: none;
            padding: 0.8rem 1.5rem;
            border-radius: 8px;
            font-size: 0.9rem;
            cursor: pointer;
            width: 100%;
            margin-top: 0.5rem;
        }
        .empty-state {
            text-align: center;
            color: #7f8c8d;
            padding: 3rem 2rem;
            font-style: italic;
            font-size: 1.1rem;
        }
        .url-preview {
            background: #f8f9fa;
            border: 1px solid #dee2e6;
            border-radius: 6px;
            padding: 0.8rem;
            font-family: monospace;
            font-size: 0.8rem;
            color: #495057;
            word-break: break-all;
            margin-top: 0.5rem;
        }
        .success-message {
            background: #d4edda;
            color: #155724;
            padding: 1rem;
            border-radius: 8px;
            margin: 1rem 0;
            border: 1px solid #c3e6cb;
        }
        .error-message {
            background: #f8d7da;
            color: #721c24;
            padding: 1rem;
            border-radius: 8px;
            margin: 1rem 0;
            border: 1px solid #f5c6cb;
        }
    </style>
</head>
<body>
    <div class="header">
        <h1>🌊⚡ QR Device Control Builder ⚡🌊</h1>
        <p>Using your proven Python QR generator - Creates REAL scannable QR codes</p>
    </div>

    <div class="container">
        <div class="panel">
            <h3>📱 Device Actions</h3>
            <button class="action-item" onclick="addAction('sms')">
                <span>📱</span>
                <span>Send SMS Message</span>
            </button>
            <button class="action-item" onclick="addAction('call')">
                <span>📞</span>
                <span>Make Phone Call</span>
            </button>
            <button class="action-item" onclick="addAction('email')">
                <span>📧</span>
                <span>Send Email</span>
            </button>
            <button class="action-item" onclick="addAction('camera')">
                <span>📷</span>
                <span>Open Camera</span>
            </button>
            <button class="action-item" onclick="addAction('maps')">
                <span>🗺️</span>
                <span>Navigate with Maps</span>
            </button>
            <button class="action-item" onclick="addAction('website')">
                <span>🌐</span>
                <span>Open Website</span>
            </button>
        </div>

        <div class="panel">
            <h3>🔄 Control Sequence Builder</h3>
            <div class="workflow-builder" id="workflowBuilder">
                <div class="empty-state">
                    Click device actions to add them to your control sequence.<br>
                    Build powerful QR workflows that execute in order!
                </div>
            </div>
        </div>

        <div class="panel">
            <h3>🎯 QR Code Generation</h3>
            <button class="generate-btn" onclick="generateQRCodes()">
                🚀 Generate REAL QR Control Sequence
            </button>
            <div id="qrContainer"></div>
        </div>
    </div>

    <script>
        let workflowSteps = [];
        let stepCounter = 0;

        const actionTemplates = {
            sms: {
                name: 'Send SMS Message',
                icon: '📱',
                fields: [
                    { key: 'phone', label: 'Phone Number', type: 'tel', placeholder: '+1-555-123-4567', required: true },
                    { key: 'message', label: 'Message Text', type: 'textarea', placeholder: 'Your message here...', required: true }
                ],
                buildUrl: (values) => `sms:${values.phone}&body=${encodeURIComponent(values.message)}`
            },
            call: {
                name: 'Make Phone Call',
                icon: '📞',
                fields: [
                    { key: 'phone', label: 'Phone Number', type: 'tel', placeholder: '+1-555-123-4567', required: true }
                ],
                buildUrl: (values) => `tel:${values.phone}`
            },
            email: {
                name: 'Send Email',
                icon: '📧',
                fields: [
                    { key: 'email', label: 'Email Address', type: 'email', placeholder: 'recipient@example.com', required: true },
                    { key: 'subject', label: 'Subject', type: 'text', placeholder: 'Email subject', required: true },
                    { key: 'body', label: 'Message Body', type: 'textarea', placeholder: 'Email content...', required: true }
                ],
                buildUrl: (values) => `mailto:${values.email}?subject=${encodeURIComponent(values.subject)}&body=${encodeURIComponent(values.body)}`
            },
            camera: {
                name: 'Open Camera',
                icon: '📷',
                fields: [],
                buildUrl: () => 'camera://'
            },
            maps: {
                name: 'Navigate with Maps',
                icon: '🗺️',
                fields: [
                    { key: 'location', label: 'Destination', type: 'text', placeholder: 'Apple Park, Cupertino, CA', required: true }
                ],
                buildUrl: (values) => `maps://?q=${encodeURIComponent(values.location)}`
            },
            website: {
                name: 'Open Website',
                icon: '🌐',
                fields: [
                    { key: 'url', label: 'Website URL', type: 'url', placeholder: 'https://example.com', required: true }
                ],
                buildUrl: (values) => values.url
            }
        };

        function addAction(actionType) {
            stepCounter++;
            const template = actionTemplates[actionType];
            
            const step = {
                id: stepCounter,
                type: actionType,
                name: template.name,
                icon: template.icon,
                fields: template.fields,
                values: {}
            };

            workflowSteps.push(step);
            renderWorkflowSteps();
        }

        function renderWorkflowSteps() {
            const container = document.getElementById('workflowBuilder');
            
            if (workflowSteps.length === 0) {
                container.innerHTML = `
                    <div class="empty-state">
                        Click device actions to add them to your control sequence.<br>
                        Build powerful QR workflows that execute in order!
                    </div>
                `;
                return;
            }

            container.innerHTML = workflowSteps.map((step, index) => {
                const fieldsHtml = step.fields.map(field => {
                    const value = step.values[field.key] || '';
                    if (field.type === 'textarea') {
                        return `
                            <div class="form-group">
                                <label>${field.label}${field.required ? ' *' : ''}</label>
                                <textarea 
                                    placeholder="${field.placeholder}" 
                                    onchange="updateStepValue(${step.id}, '${field.key}', this.value)"
                                    rows="3"
                                >${value}</textarea>
                            </div>
                        `;
                    } else {
                        return `
                            <div class="form-group">
                                <label>${field.label}${field.required ? ' *' : ''}</label>
                                <input 
                                    type="${field.type}" 
                                    placeholder="${field.placeholder}" 
                                    value="${value}"
                                    onchange="updateStepValue(${step.id}, '${field.key}', this.value)"
                                />
                            </div>
                        `;
                    }
                }).join('');

                const url = buildStepUrl(step);
                const urlPreview = url ? `<div class="url-preview">URL: ${url}</div>` : '';

                return `
                    <div class="workflow-step">
                        <div class="step-number">${index + 1}</div>
                        <button class="remove-btn" onclick="removeStep(${step.id})">&times;</button>
                        <h4>${step.icon} ${step.name}</h4>
                        ${fieldsHtml}
                        ${urlPreview}
                    </div>
                `;
            }).join('');
        }

        function updateStepValue(stepId, key, value) {
            const step = workflowSteps.find(s => s.id === stepId);
            if (step) {
                step.values[key] = value;
                renderWorkflowSteps();
            }
        }

        function removeStep(stepId) {
            workflowSteps = workflowSteps.filter(s => s.id !== stepId);
            renderWorkflowSteps();
        }

        function buildStepUrl(step) {
            const template = actionTemplates[step.type];
            if (!template) return '';

            const hasAllRequired = template.fields
                .filter(f => f.required)
                .every(f => step.values[f.key] && step.values[f.key].trim());

            if (!hasAllRequired && template.fields.some(f => f.required)) {
                return '';
            }

            try {
                let url = template.buildUrl(step.values);
                const nonce = Math.random().toString(36).substring(2, 15);
                const timestamp = Math.floor(Date.now() / 1000);
                const separator = url.includes('?') ? '&' : '?';
                url += `${separator}nonce=${nonce}&ts=${timestamp}`;
                return url;
            } catch (e) {
                return '';
            }
        }

        async function generateQRCodes() {
            const container = document.getElementById('qrContainer');
            
            if (workflowSteps.length === 0) {
                container.innerHTML = '<div class="error-message">Please add some actions to your workflow first!</div>';
                return;
            }

            const invalidSteps = workflowSteps.filter(step => {
                const template = actionTemplates[step.type];
                return template.fields
                    .filter(f => f.required)
                    .some(f => !step.values[f.key] || !step.values[f.key].trim());
            });

            if (invalidSteps.length > 0) {
                container.innerHTML = '<div class="error-message">Please fill in all required fields (marked with *) before generating QR codes.</div>';
                return;
            }

            container.innerHTML = '<div class="success-message">🔄 Generating REAL QR codes using your proven Python system...</div>';

            // Prepare actions data
            const actionsData = workflowSteps.map((step, index) => ({
                step: index + 1,
                description: step.name,
                url: buildStepUrl(step)
            }));

            try {
                const response = await fetch('/generate_qr', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({ actions: actionsData })
                });

                const result = await response.json();

                if (result.success) {
                    container.innerHTML = '<div class="success-message">✅ QR codes generated successfully!</div>';
                    
                    result.qr_codes.forEach((qr, index) => {
                        const qrDiv = document.createElement('div');
                        qrDiv.className = 'qr-item';
                        
                        qrDiv.innerHTML = `
                            <h4>Step ${index + 1}: ${workflowSteps[index].icon} ${workflowSteps[index].name}</h4>
                            <img src="data:image/png;base64,${qr.image_data}" class="qr-image" alt="QR Code" />
                            <div class="url-preview">${qr.url}</div>
                            <button class="download-btn" onclick="downloadQR('data:image/png;base64,${qr.image_data}', '${qr.filename}')">
                                📥 Download ${qr.filename}
                            </button>
                        `;
                        
                        container.appendChild(qrDiv);
                    });
                } else {
                    container.innerHTML = `<div class="error-message">Error: ${result.error}</div>`;
                }
            } catch (error) {
                container.innerHTML = `<div class="error-message">Network error: ${error.message}</div>`;
            }
        }

        function downloadQR(dataUrl, filename) {
            const link = document.createElement('a');
            link.download = filename;
            link.href = dataUrl;
            document.body.appendChild(link);
            link.click();
            document.body.removeChild(link);
        }
    </script>
</body>
</html>'''
        
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(html_content.encode())
    
    def handle_generate_qr(self):
        try:
            if self.command == 'POST':
                content_length = int(self.headers['Content-Length'])
                post_data = self.rfile.read(content_length)
                data = json.loads(post_data.decode('utf-8'))
                actions = data.get('actions', [])
            else:
                actions = []
            
            if not actions:
                self.send_json_response({'success': False, 'error': 'No actions provided'})
                return
            
            # Create temporary JSON file
            temp_json = 'temp_web_actions.json'
            with open(temp_json, 'w') as f:
                json.dump(actions, f, indent=2)
            
            # Run your proven QR generator
            cmd = [
                "python3", "qr_phone_control_loop.py",
                "--actions", temp_json,
                "--ecc", "Q",
                "--delay", "0.1"
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True, cwd=os.getcwd())
            
            if result.returncode == 0:
                # Find generated QR files
                qr_files = []
                for i, action in enumerate(actions):
                    qr_filename = f"QR_CONTROL_LOOP_STEP_{i+1}.png"
                    if os.path.exists(qr_filename):
                        with open(qr_filename, 'rb') as f:
                            image_data = base64.b64encode(f.read()).decode('utf-8')
                        qr_files.append({
                            'filename': qr_filename,
                            'image_data': image_data,
                            'url': action['url']
                        })
                
                # Clean up temp file
                if os.path.exists(temp_json):
                    os.remove(temp_json)
                
                self.send_json_response({
                    'success': True,
                    'qr_codes': qr_files,
                    'message': f'Generated {len(qr_files)} QR codes'
                })
            else:
                self.send_json_response({
                    'success': False,
                    'error': result.stderr or 'QR generation failed',
                    'stdout': result.stdout
                })
            
        except Exception as e:
            self.send_json_response({'success': False, 'error': str(e)})
    
    def send_json_response(self, data):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(json.dumps(data).encode())
    
    def log_message(self, format, *args):
        pass

def start_server(port=8080):
    server = HTTPServer(('localhost', port), QRWebHandler)
    print(f"🚀 QR Control Builder running at http://localhost:{port}")
    print("📱 Using your PROVEN Python QR generator!")
    print("🔄 Press Ctrl+C to stop the server")
    
    def open_browser():
        time.sleep(1)
        webbrowser.open(f'http://localhost:{port}')
    
    threading.Thread(target=open_browser, daemon=True).start()
    
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n🛑 Server stopped")
        server.shutdown()

if __name__ == "__main__":
    start_server()
