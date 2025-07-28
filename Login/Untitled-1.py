import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtCore import QUrl

class WebGLViewer(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("نمایشگر WebGL با PyQt5")
        self.resize(800, 600)
        
        # ایجاد ویجت مرکزی
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # ایجاد لیآوت
        layout = QVBoxLayout()
        central_widget.setLayout(layout)
        
        # ایجاد مرورگر وب
        self.browser = QWebEngineView()
        
        # بارگذاری یک صفحه وب با WebGL
        html_content = """
        <!DOCTYPE html>
        <html>
        <head>
            <title>WebGL Demo</title>
            <style>
                body { margin: 0; overflow: hidden; }
                canvas { display: block; }
            </style>
        </head>
        <body>
            <canvas id="glCanvas"></canvas>
            
            <script>
                const canvas = document.getElementById('glCanvas');
                const gl = canvas.getContext('webgl');
                
                // تنظیم اندازه کانواس به اندازه پنجره
                canvas.width = window.innerWidth;
                canvas.height = window.innerHeight;
                
                // تنظیم رنگ پس‌زمینه
                gl.clearColor(0.2, 0.3, 0.8, 1.0);
                gl.clear(gl.COLOR_BUFFER_BIT);
                
                // ایجاد مثلث ساده با WebGL
                const vertices = [
                     0.0,  0.5, 0.0,
                    -0.5, -0.5, 0.0,
                     0.5, -0.5, 0.0
                ];
                
                const vertexBuffer = gl.createBuffer();
                gl.bindBuffer(gl.ARRAY_BUFFER, vertexBuffer);
                gl.bufferData(gl.ARRAY_BUFFER, new Float32Array(vertices), gl.STATIC_DRAW);
                
                // شیدرهای ساده
                const vsSource = `
                    attribute vec3 coordinates;
                    void main(void) {
                        gl_Position = vec4(coordinates, 1.0);
                    }
                `;
                
                const fsSource = `
                    void main(void) {
                        gl_FragColor = vec4(0.9, 0.3, 0.2, 1.0);
                    }
                `;
                
                // کامپایل شیدرها
                const vertexShader = gl.createShader(gl.VERTEX_SHADER);
                gl.shaderSource(vertexShader, vsSource);
                gl.compileShader(vertexShader);
                
                const fragmentShader = gl.createShader(gl.FRAGMENT_SHADER);
                gl.shaderSource(fragmentShader, fsSource);
                gl.compileShader(fragmentShader);
                
                // ایجاد برنامه شیدر
                const shaderProgram = gl.createProgram();
                gl.attachShader(shaderProgram, vertexShader);
                gl.attachShader(shaderProgram, fragmentShader);
                gl.linkProgram(shaderProgram);
                gl.useProgram(shaderProgram);
                
                // اتصال attributeها
                gl.bindBuffer(gl.ARRAY_BUFFER, vertexBuffer);
                const coord = gl.getAttribLocation(shaderProgram, "coordinates");
                gl.vertexAttribPointer(coord, 3, gl.FLOAT, false, 0, 0);
                gl.enableVertexAttribArray(coord);
                
                // رسم مثلث
                gl.drawArrays(gl.TRIANGLES, 0, 3);
            </script>
        </body>
        </html>
        """
        
        # بارگذاری محتوای HTML
        self.browser.setHtml(html_content, QUrl("about:blank"))
        layout.addWidget(self.browser)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    # فعال کردن WebGL
    settings = QWebEngineView().settings()
    settings.setAttribute(settings.WebGLEnabled, True)
    settings.setAttribute(settings.Accelerated2dCanvasEnabled, True)
    
    window = WebGLViewer()
    window.show()
    sys.exit(app.exec_())