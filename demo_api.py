#!/usr/bin/env python3
"""
Simple Tire Defect Detection API Demo
No dependencies required - uses only Python standard library
Run with: python demo_api.py
"""

import json
import http.server
import socketserver
import urllib.parse
from datetime import datetime
import webbrowser
import threading
import time

class DemoAPIHandler(http.server.BaseHTTPRequestHandler):
    
    def do_GET(self):
        # Parse the URL
        parsed_path = urllib.parse.urlparse(self.path)
        path = parsed_path.path
        
        # Route handling
        if path == '/':
            self.send_homepage()
        elif path == '/health':
            self.send_health()
        elif path == '/docs':
            self.send_api_docs()
        elif path == '/api/v1/analytics/summary':
            self.send_analytics()
        else:
            self.send_404()
    
    def do_POST(self):
        parsed_path = urllib.parse.urlparse(self.path)
        path = parsed_path.path
        
        if path == '/api/v1/detect':
            self.send_detection_result()
        else:
            self.send_404()
    
    def send_homepage(self):
        html = """
        <!DOCTYPE html>
        <html>
        <head>
            <title>🛞 Tire Defect Detection System</title>
            <style>
                body { font-family: Arial, sans-serif; margin: 40px; background: #f5f5f5; }
                .header { background: #2c3e50; color: white; padding: 20px; border-radius: 8px; }
                .content { background: white; padding: 20px; margin: 20px 0; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }
                .endpoint { background: #ecf0f1; padding: 15px; margin: 10px 0; border-radius: 5px; }
                .status { color: #27ae60; font-weight: bold; }
                .metric { display: inline-block; margin: 10px 20px 10px 0; padding: 10px; background: #3498db; color: white; border-radius: 5px; }
                a { color: #3498db; text-decoration: none; }
                a:hover { text-decoration: underline; }
            </style>
        </head>
        <body>
            <div class="header">
                <h1>🛞 Enterprise Tire Defect Detection System</h1>
                <p>Edge AI IoT solution for real-time tire defect detection in manufacturing environments</p>
                <p><strong>Developed for David Linthicum's Enterprise AI Architecture Program</strong></p>
            </div>
            
            <div class="content">
                <h2>🎯 System Status</h2>
                <p class="status">✅ System Online - All Services Running</p>
                
                <div class="metric">Processed Today: 1,247 tires</div>
                <div class="metric">Accuracy: 92.5%</div>
                <div class="metric">Avg Response: 245ms</div>
                <div class="metric">Defects Found: 89</div>
            </div>
            
            <div class="content">
                <h2>🔧 API Endpoints</h2>
                
                <div class="endpoint">
                    <strong>GET <a href="/health">/health</a></strong><br>
                    System health check and performance metrics
                </div>
                
                <div class="endpoint">
                    <strong>POST /api/v1/detect</strong><br>
                    Real-time tire defect detection (send image data)
                </div>
                
                <div class="endpoint">
                    <strong>GET <a href="/api/v1/analytics/summary">/api/v1/analytics/summary</a></strong><br>
                    Daily analytics and business metrics
                </div>
                
                <div class="endpoint">
                    <strong>GET <a href="/docs">/docs</a></strong><br>
                    Interactive API documentation
                </div>
            </div>
            
            <div class="content">
                <h2>🏗️ Architecture Features</h2>
                <ul>
                    <li><strong>YOLOv8 Computer Vision:</strong> Sub-500ms inference time</li>
                    <li><strong>Enterprise Security:</strong> Authentication, rate limiting, audit logging</li>
                    <li><strong>Microservices Design:</strong> Scalable container-based deployment</li>
                    <li><strong>Real-time Processing:</strong> 24/7 automated quality control</li>
                    <li><strong>ERP Integration:</strong> SAP S/4HANA ready APIs</li>
                </ul>
            </div>
            
            <div class="content">
                <h2>💰 Business Value</h2>
                <ul>
                    <li><strong>Cost Savings:</strong> $200K+ per production line annually</li>
                    <li><strong>Quality Improvement:</strong> 20x faster than manual inspection</li>
                    <li><strong>Risk Reduction:</strong> Prevents multi-million dollar recalls</li>
                    <li><strong>Operational Excellence:</strong> 24/7 continuous monitoring</li>
                </ul>
            </div>
        </body>
        </html>
        """
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(html.encode())
    
    def send_health(self):
        data = {
            "status": "healthy",
            "timestamp": datetime.now().isoformat(),
            "services": {
                "api": "running",
                "ai_model": "loaded",
                "database": "connected",
                "messaging": "active"
            },
            "performance": {
                "inference_time_ms": 245,
                "accuracy_percent": 92.5,
                "processed_today": 1247,
                "uptime_hours": 72.3
            },
            "system_resources": {
                "cpu_usage_percent": 23.4,
                "memory_usage_percent": 45.2,
                "disk_usage_percent": 67.8
            }
        }
        self.send_json_response(data)
    
    def send_detection_result(self):
        data = {
            "detection_id": f"TD-2025-{int(time.time())}",
            "timestamp": datetime.now().isoformat(),
            "image_info": {
                "resolution": "1920x1080",
                "format": "jpeg",
                "size_bytes": 245760
            },
            "defects_found": [
                {
                    "type": "sidewall_crack",
                    "confidence": 0.94,
                    "severity": "high",
                    "location": {"x": 120, "y": 45, "width": 60, "height": 50},
                    "description": "Vertical crack in sidewall, 2.3cm length"
                },
                {
                    "type": "tread_separation",
                    "confidence": 0.87,
                    "severity": "medium", 
                    "location": {"x": 200, "y": 150, "width": 80, "height": 50},
                    "description": "Partial tread separation detected"
                }
            ],
            "overall_quality": "REJECT",
            "recommendation": "Do not ship - critical defects detected",
            "processing_time_ms": 245,
            "next_actions": [
                "Quarantine tire for detailed inspection",
                "Update quality control logs",
                "Notify production supervisor"
            ]
        }
        self.send_json_response(data)
    
    def send_analytics(self):
        data = {
            "daily_stats": {
                "date": datetime.now().strftime("%Y-%m-%d"),
                "tires_processed": 1247,
                "defects_detected": 89,
                "defect_rate_percent": 7.1,
                "avg_processing_time_ms": 245,
                "rejected_tires": 89,
                "passed_tires": 1158
            },
            "quality_metrics": {
                "accuracy_percent": 92.5,
                "false_positives_percent": 2.1,
                "false_negatives_percent": 1.8,
                "precision": 0.925,
                "recall": 0.913
            },
            "performance_trends": {
                "throughput_increase_percent": 15.3,
                "accuracy_improvement_percent": 3.2,
                "downtime_reduction_percent": 78.5
            },
            "cost_savings": {
                "labor_saved_hours": 156,
                "estimated_daily_savings_usd": 4680,
                "defects_prevented": 89,
                "recall_risk_reduction_percent": 85.2
            },
            "production_impact": {
                "lines_monitored": 3,
                "facilities_covered": 1,
                "monthly_volume": 37410,
                "quality_score": 9.25
            }
        }
        self.send_json_response(data)
    
    def send_api_docs(self):
        docs_html = """
        <!DOCTYPE html>
        <html>
        <head>
            <title>API Documentation - Tire Defect Detection</title>
            <style>
                body { font-family: Arial, sans-serif; margin: 40px; background: #f8f9fa; }
                .header { background: #007bff; color: white; padding: 20px; border-radius: 8px; }
                .endpoint { background: white; margin: 20px 0; padding: 20px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }
                .method { padding: 5px 10px; border-radius: 3px; color: white; font-weight: bold; }
                .get { background: #28a745; }
                .post { background: #007bff; }
                .response { background: #f8f9fa; padding: 15px; border-radius: 5px; margin: 10px 0; }
                pre { background: #e9ecef; padding: 15px; border-radius: 5px; overflow-x: auto; }
                .test-button { background: #28a745; color: white; padding: 10px 15px; border: none; border-radius: 5px; cursor: pointer; }
                .test-button:hover { background: #218838; }
            </style>
        </head>
        <body>
            <div class="header">
                <h1>🔧 Tire Defect Detection API Documentation</h1>
                <p>Interactive API reference for enterprise integration</p>
            </div>
            
            <div class="endpoint">
                <h3><span class="method get">GET</span> /health</h3>
                <p>System health check and performance monitoring</p>
                <button class="test-button" onclick="testEndpoint('/health')">Test Endpoint</button>
                <div class="response">
                    <strong>Response Example:</strong>
                    <pre>{
  "status": "healthy",
  "services": {"api": "running", "ai_model": "loaded"},
  "performance": {"inference_time_ms": 245, "accuracy_percent": 92.5}
}</pre>
                </div>
            </div>
            
            <div class="endpoint">
                <h3><span class="method post">POST</span> /api/v1/detect</h3>
                <p>Real-time tire defect detection</p>
                <button class="test-button" onclick="testDetection()">Test Detection</button>
                <div class="response">
                    <strong>Request:</strong> Send tire image data (multipart/form-data)<br>
                    <strong>Response:</strong> Defect analysis with locations and confidence scores
                </div>
            </div>
            
            <div class="endpoint">
                <h3><span class="method get">GET</span> /api/v1/analytics/summary</h3>
                <p>Daily analytics and business metrics</p>
                <button class="test-button" onclick="testEndpoint('/api/v1/analytics/summary')">Test Analytics</button>
                <div class="response">
                    <strong>Response:</strong> Production statistics, quality metrics, cost savings
                </div>
            </div>
            
            <script>
                function testEndpoint(url) {
                    window.open(url, '_blank');
                }
                
                function testDetection() {
                    fetch('/api/v1/detect', {method: 'POST'})
                        .then(response => response.json())
                        .then(data => {
                            alert('Detection Result: ' + data.overall_quality + '\\nProcessing Time: ' + data.processing_time_ms + 'ms');
                        });
                }
            </script>
        </body>
        </html>
        """
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(docs_html.encode())
    
    def send_json_response(self, data):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(json.dumps(data, indent=2).encode())
    
    def send_404(self):
        self.send_response(404)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        error = {"error": "Not Found", "message": "The requested endpoint does not exist"}
        self.wfile.write(json.dumps(error).encode())

def start_demo_server():
    PORT = 8000
    with socketserver.TCPServer(("", PORT), DemoAPIHandler) as httpd:
        print(f"""
🎉 Tire Defect Detection Demo Server Started!

📊 Dashboard:        http://localhost:{PORT}
🔧 API Docs:         http://localhost:{PORT}/docs  
📋 Health Check:     http://localhost:{PORT}/health
📈 Analytics:        http://localhost:{PORT}/api/v1/analytics/summary

Press Ctrl+C to stop the server
        """)
        
        # Auto-open browser after 2 seconds
        def open_browser():
            time.sleep(2)
            try:
                webbrowser.open(f'http://localhost:{PORT}')
            except:
                pass
        
        threading.Thread(target=open_browser, daemon=True).start()
        
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nShutting down demo server...")

if __name__ == "__main__":
    start_demo_server()
