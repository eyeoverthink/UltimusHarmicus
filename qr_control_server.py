#!/usr/bin/env python3
"""
QR Control Server - Local server that generates real QR codes for the web interface
Uses the proven qrcode library from qr_phone_control_loop.py
"""

import qrcode
import json
import base64
from io import BytesIO
from http.server import HTTPServer, BaseHTTPRequestHandler
import urllib.parse
import threading
import webbrowser
import time

class QRHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            self.serve_html()
        elif self.path.startswith('/generate_qr'):
            self.generate_qr()
        else:
            self.send_error(404)
    
    def do_POST(self):
        if self.path == '/generate_qr':
            self.generate_qr()
        else:
            self.send_error(404)
    
    def serve_html(self):
        html_content = '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>QR Device Control Builder - Professional</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

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
            display: flex;
            align-items: center;
            gap: 0.5rem;
        }

        .device-actions {
            overflow-y: auto;
            max-height: calc(100vh - 240px);
        }

        .action-category {
            margin-bottom: 2rem;
        }

        .category-title {
            font-size: 0.9rem;
            font-weight: 700;
            color: #7f8c8d;
            margin-bottom: 1rem;
            text-transform: uppercase;
            letter-spacing: 1px;
            border-bottom: 2px solid #ecf0f1;
            padding-bottom: 0.5rem;
        }

        .action-item {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 1rem 1.2rem;
            margin-bottom: 0.8rem;
            border-radius: 12px;
            cursor: pointer;
            transition: all 0.3s ease;
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
            position: relative;
            overflow-y: auto;
            max-height: calc(100vh - 240px);
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

        .workflow-step .step-number {
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
    </style>
</head>
<body>
    <div class="header">
        <h1>🌊⚡ QR Device Control Builder ⚡🌊</h1>
        <p>Create powerful QR sequences that control your iPhone - Revolutionary device programming</p>
    </div>

    <div class="container">
        <div class="panel">
            <h3>📱 Device Actions</h3>
            <div class="device-actions">
                <div class="action-category">
                    <div class="category-title">Communication</div>
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
                </div>
                <div class="action-category">
                    <div class="category-title">Apps & Media</div>
                    <button class="action-item" onclick="addAction('camera')">
                        <span>📷</span>
                        <span>Open Camera</span>
                    </button>
                    <button class="action-item" onclick="addAction('maps')">
                        <span>🗺️</span>
                        <span>Navigate with Maps</span>
                    </button>
                </div>
                <div class="action-category">
                    <div class="category-title">Web</div>
                    <button class="action-item" onclick="addAction('website')">
                        <span>🌐</span>
                        <span>Open Website</span>
                    </button>
                </div>
            </div>
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
            <div class="qr-preview">
                <button class="generate-btn" onclick="generateQRCodes()">
                    🚀 Generate QR Control Sequence
                </button>
                <div id="qrContainer"></div>
            </div>
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
                container.innerHTML = '<div style="color: red;">Please add some actions to your workflow first!</div>';
                return;
            }

            const invalidSteps = workflowSteps.filter(step => {
                const template = actionTemplates[step.type];
                return template.fields
                    .filter(f => f.required)
                    .some(f => !step.values[f.key] || !step.values[f.key].trim());
            });

            if (invalidSteps.length > 0) {
                container.innerHTML = '<div style="color: red;">Please fill in all required fields (marked with *) before generating QR codes.</div>';
                return;
            }

            container.innerHTML = '<div style="color: #667eea;">🔄 Generating real QR codes...</div>';

            try {
                container.innerHTML = '';

                for (let i = 0; i < workflowSteps.length; i++) {
                    const step = workflowSteps[i];
                    const url = buildStepUrl(step);
                    if (!url) continue;

                    const response = await fetch('/generate_qr?url=' + encodeURIComponent(url));
                    const result = await response.json();

                    if (result.success) {
                        const qrDiv = document.createElement('div');
                        qrDiv.className = 'qr-item';
                        
                        qrDiv.innerHTML = `
                            <h4>Step ${i + 1}: ${step.icon} ${step.name}</h4>
                            <img src="${result.data_url}" class="qr-image" alt="QR Code" />
                            <button class="download-btn" onclick="downloadQR('${result.data_url}', 'qr-step-${i + 1}-${step.type}.png')">
                                📥 Download Step ${i + 1}
                            </button>
                        `;
                        
                        container.appendChild(qrDiv);
                    } else {
                        container.innerHTML += `<div style="color: red;">Error generating QR for step ${i + 1}: ${result.error}</div>`;
                    }
                }
            } catch (error) {
                container.innerHTML = `<div style="color: red;">Error: ${error.message}</div>`;
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
    
    def generate_qr(self):
        try:
            # Parse URL parameter
            if '?' in self.path:
                query = urllib.parse.urlparse(self.path).query
                params = urllib.parse.parse_qs(query)
                url = params.get('url', [''])[0]
            else:
                url = ''
            
            if not url:
                self.send_json_response({'success': False, 'error': 'No URL provided'})
                return
            
            # Generate QR code using the proven qrcode library
            qr = qrcode.QRCode(
                version=1,
                error_correction=qrcode.constants.ERROR_CORRECT_M,
                box_size=10,
                border=4,
            )
            qr.add_data(url)
            qr.make(fit=True)
            
            # Create image
            img = qr.make_image(fill_color="black", back_color="white")
            
            # Convert to data URL
            buffer = BytesIO()
            img.save(buffer, format='PNG')
            img_str = base64.b64encode(buffer.getvalue()).decode()
            data_url = f"data:image/png;base64,{img_str}"
            
            self.send_json_response({'success': True, 'data_url': data_url})
            
        except Exception as e:
            self.send_json_response({'success': False, 'error': str(e)})
    
    def send_json_response(self, data):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(json.dumps(data).encode())
    
    def log_message(self, format, *args):
        # Suppress default logging
        pass

def start_server(port=8080):
    server = HTTPServer(('localhost', port), QRHandler)
    print(f"🚀 QR Control Builder running at http://localhost:{port}")
    print("📱 Add your actions and generate real QR codes!")
    print("🔄 Press Ctrl+C to stop the server")
    
    # Open browser after a short delay
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
