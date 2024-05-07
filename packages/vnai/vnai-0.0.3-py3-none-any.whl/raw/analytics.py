import os
import pathlib
# import pkg_resources
import importlib.metadata
import asyncio
import requests
import psutil
import platform
import uuid
import sys
import socket

class VnstockInitializer:
    def __init__(self, hook_id):
        # Define terms and conditions
        self.TERMS_AND_CONDITIONS = """
        THOẢ THUẬN SỬ DỤNG - ĐIỀU KHOẢN & ĐIỀU KIỆN SỬ DỤNG VNSTOCK3
        ------------------------
        Khi sử dụng vnstock, bạn xác nhận rằng bạn đã đọc, hiểu rõ, và chấp nhận các điều khoản mô tả dưới đây. Vui lòng nhập 'Tôi đồng ý' hoặc nhấn Enter để chấp nhận các điều khoản và điều kiện này và tiếp tục sử dụng phần mềm.

        I. ĐIỀU KHOẢN CHUNG
        ------------------------
        - Thư viện này chỉ dành cho mục đích cá nhân và không được phân phối lại hoặc sử dụng cho mục đích thương mại mà không có sự đồng ý bằng văn bản chính thức từ tác giả. Tất cả bản quyền và sở hữu trí tuệ thuộc về tác giả. Bất kỳ hành vi vi phạm bản quyền hoặc sở hữu trí tuệ sẽ bị xử lý theo pháp luật.

        - Bạn không được sử dụng thư viện này cho các mục đích bất hợp pháp, phi đạo đức, hoặc trái với quy định pháp luật hiện hành.

        - Bạn đồng ý rằng tác giả không chịu trách nhiệm cho bất kỳ thiệt hại, mất mát, hoặc hậu quả nào phát sinh từ việc sử dụng thư viện này, đặc biệt trong hoạt động đầu tư hoặc bất kỳ hoạt động nào có rủi ro. Bạn tự chịu trách nhiệm cho các quyết định đầu tư của mình.

        - Bạn đồng ý tuân thủ mọi luật pháp, quy định, và hướng dẫn liên quan khi sử dụng thư viện này.

        - Bạn chấp nhận rằng thư viện này có thể lưu trữ dữ liệu cục bộ để lưu cấu hình, cung cấp tính năng cá nhân hóa, hoặc cho mục đích phân tích. Thông tin này sẽ được bảo mật và không được chia sẻ với bên thứ ba mà không có sự đồng ý của bạn.

        II. LƯU TRỮ & XỬ LÝ DỮ LIỆU
        ------------------------
        Thư viện này thu thập dữ liệu để phân tích, thống kê, và cải thiện hiệu suất. Dữ liệu này được lưu trữ cục bộ và không được chia sẻ với bên thứ ba. Dưới đây là danh sách các thông tin được thu thập, cùng với giải thích và ví dụ mẫu:

        - UUID (Machine ID): Một định danh duy nhất cho máy tính của bạn, giúp phân biệt các thiết bị. Ví dụ: "123e4567-e89b-12d3-a456-426614174000".

        - Environment (Môi trường): Mô tả môi trường chạy chương trình, như "development", "testing", hoặc "production". Ví dụ: "production".

        - Python Version (Phiên bản Python): Phiên bản Python đang chạy trên hệ thống của bạn. Ví dụ: "3.9.1".

        - OS Name (Tên hệ điều hành): Tên hệ điều hành đang chạy trên máy tính. Ví dụ: "Windows".

        - OS Version (Phiên bản hệ điều hành): Phiên bản cụ thể của hệ điều hành. Ví dụ: "10.0.19041".

        - Machine (Máy): Mô tả loại máy tính hoặc kiến trúc phần cứng. Ví dụ: "AMD64".

        - CPU Model (Mô hình CPU): Thông tin về loại bộ xử lý (CPU) trên máy tính. Ví dụ: "Intel Core i7-8700".

        - CPU Cores (Số lõi CPU): Số lõi vật lý của CPU. Ví dụ: 6.

        - CPU Logical Cores (Số lõi CPU logic): Số lõi logic của CPU, thường bao gồm cả lõi vật lý và lõi ảo. Ví dụ: 12.

        - RAM Total (Tổng dung lượng RAM): Tổng dung lượng bộ nhớ RAM trên máy tính, tính bằng gigabyte (GB). Ví dụ: 16.0 GB.

        - RAM Available (Dung lượng RAM có sẵn): Dung lượng bộ nhớ RAM còn trống, tính bằng gigabyte (GB). Ví dụ: 8.5 GB.

        - Local IP (Địa chỉ IP cục bộ): Địa chỉ IP cục bộ của máy tính.

        - MAC Address (Địa chỉ MAC): Địa chỉ MAC (Media Access Control) của thiết bị mạng. Ví dụ: "00:1A:A2:3B:4C:5D".
        """

        self.HOME_DIR = pathlib.Path.home()
        self.PROJECT_DIR = self.HOME_DIR / ".vnstock"
        self.TERMS_FILE_PATH = self.PROJECT_DIR / "terms_agreement.txt"

        # Create the project directory if it doesn't exist
        self.PROJECT_DIR.mkdir(exist_ok=True)
        self.hook_id = hook_id

    async def system_info(self):
        """
        Gathers information about the environment and system.
        """
        # Generate UUID
        machine_id = str(uuid.uuid4())

        # Environment (modify to detect your specific frameworks)
        try:
            from IPython import get_ipython
            if 'IPKernelApp' not in get_ipython().config:  # Check if not in IPython kernel
                if sys.stdout.isatty():
                    environment = "Terminal"
                else:
                    environment = "Other"  # Non-interactive environment (e.g., script executed from an IDE)
            else:
                environment = "Jupyter"
        except (ImportError, AttributeError):
            # Fallback if IPython isn't installed or other checks fail
            if sys.stdout.isatty():
                environment = "Terminal"
            else:
                environment = "Other"

        # System information
        os_info = platform.uname()

        # CPU information
        cpu_arch = platform.processor()  
        cpu_logical_cores = psutil.cpu_count(logical=True)
        cpu_cores = psutil.cpu_count(logical=False)

        # Memory information
        ram_total = psutil.virtual_memory().total / (1024**3)  # GB
        ram_available = psutil.virtual_memory().available / (1024**3)  # GB

        hostname = socket.gethostname()
        IPAddr = socket.gethostbyname(hostname)

        mac = ':'.join(['{:02x}'.format((uuid.getnode() >> elements) & 0xff) for elements in range(0, 2 * 6, 2)])

        # Combine information into a dictionary
        info = {
            "uuid": machine_id,
            "environment": environment,
            "python_version": platform.python_version(),
            "os_name": os_info.system,
            "os_version": os_info.version,
            "machine": os_info.machine,
            "cpu_model": cpu_arch,
            "cpu_cores": cpu_cores,
            "cpu_logical_cores": cpu_logical_cores,
            "ram_total": round(ram_total, 1),
            "ram_available": round(ram_available, 1),
            "local_ip": IPAddr,
            "mac_address": mac,
        }

        return info

    async def show_terms_and_conditions(self):
        """
        Displays terms and conditions and asks for acceptance.
        """
        print(self.TERMS_AND_CONDITIONS)

        response = input("Nhập 'Tôi đồng ý' hoặc nhấn Enter để chấp nhận: ")
        
        # If the user presses Enter without typing, default to "Tôi đồng ý"
        if not response.strip():
            response = "tôi đồng ý"

        if response.strip().lower() == "tôi đồng ý":
            from datetime import datetime
            # get now time in string
            now = datetime.now()
            HARDWARE = await self.system_info()
            # VERSION = pkg_resources.get_distribution('vnstock').version
            
            VERSION = None
            try:
                VERSION = importlib.metadata.version('vnstock')
            except importlib.metadata.PackageNotFoundError:
                print("Package 'vnstock' not found")

            # parse HARDWARE to string to store in the file
            signed_aggreement = f"PHIÊN BẢN: {VERSION}\nMÔ TẢ:\nNgười dùng có mã nhận dạng {HARDWARE['uuid']} đã chấp nhận điều khoản & điều kiện sử dụng Vnstock lúc {now}\n---\n\nTHÔNG TIN THIẾT BỊ: {str(HARDWARE)}\n\nĐính kèm bản sao nội dung bạn đã đọc, hiểu rõ và đồng ý dưới đây:\n{self.TERMS_AND_CONDITIONS}"
            # Store the acceptance
            with open(self.TERMS_FILE_PATH, "w", encoding="utf-8") as f:
                f.write(signed_aggreement)
            print("---\nCảm ơn bạn đã chấp nhận điều khoản và điều kiện!\nBạn đã có thể tiếp tục sử dụng Vnstock!\nBạn có thể xem lại điều khoản và điều kiện tại đường dẫn sau: ", self.TERMS_FILE_PATH)
            return True
        else:
            return False

    async def send_analytics_data(self):
        """
        Sends analytics data to a webhook.
        """
        HARDWARE = await self.system_info()
        WEBHOOK_URI = f"https://botbuilder.larksuite.com/api/trigger-webhook/{self.hook_id}"

        data = {
            "systems": HARDWARE,
            "accepted_agreement": True,
            "installed_packages": await self.packages_installed(),
        }

        try:
            response = requests.post(WEBHOOK_URI, json=data)
        except:
            raise SystemExit("Không thể gửi dữ liệu phân tích. Vui lòng kiểm tra kết nối mạng và thử lại sau.")

    async def check_terms_accepted(self):
        """
        Checks if terms and conditions are accepted.
        """
        if not self.TERMS_FILE_PATH.exists():
            # If not, ask for acceptance
            accepted = await self.show_terms_and_conditions()
            if not accepted:
                raise SystemExit("Điều khoản và điều kiện không được chấp nhận. Không thể tiếp tục.")
            else:
                await self.send_analytics_data()

    async def packages_installed(self):
        """
        Checks installed packages and returns a dictionary.
        """
        # Define package mapping
        package_mapping = {
                    "vnstock_family": [
                        "vnstock",
                        "vnstock3",
                        "vnstock_ezchart",
                        "vnstock_data_pro"
                        "vnstock_market_data_pipeline",
                        "vnstock_ta"
                    ],

                    # Analytics
                    "analytics": [
                        "openbb",
                        "pandas_ta"
                    ],

                    # Static charts
                    "static_charts": [
                        "matplotlib",
                        "seaborn",
                        "altair"
                    ],

                    # Dashboard
                    "dashboard": [
                        "streamlit",
                        "voila",
                        "panel"
                    ],

                    # Interactive charts
                    "interactive_charts": [
                        "mplfinance",
                        "plotly",
                        "plotline",
                        "bokeh",
                        "pyecharts",
                        "highcharts-core",
                        "highcharts-stock"
                    ],

                    # Datafeed
                    "datafeed": [
                        "yfinance",
                        "alpha_vantage",
                        "pandas-datareader",
                        "investpy",
                    ],

                    # Official API
                    "official_api": [
                        "ssi-fc-data",
                        "ssi-fctrading"
                    ],

                    # Risk & Return
                    "risk_return": [
                        "pyfolio",
                        "empyrical",
                        "quantstats"
                    ],

                    # Machine learning
                    "machine_learning": [
                        "scipy",
                        "sklearn",
                        "statsmodels",
                        "pytorch",
                        "tensorflow",
                        "keras",
                        "xgboost"
                    ],

                    # Indicators
                    "indicators": [
                        "stochastic",
                        "talib",
                        "tqdm",
                        "finta",
                        "financetoolkit",
                        "tulipindicators"
                    ],

                    # Backtesting
                    "backtesting": [
                        "vectorbt",
                        "backtesting",
                        "bt",
                        "zipline",
                        "pyalgotrade",
                        "backtrader",
                        "pybacktest"
                    ],

                    # Server
                    "server": [
                        "fastapi",
                        "flask",
                        "uvicorn",
                        "gunicorn"
                    ],

                    # Framework
                    "framework": [
                        "lightgbm",
                        "catboost",
                        "django",
                    ]
                }

        # installed_packages = {}

        # for category, packages in package_mapping.items():
        #     installed_packages[category] = []
        #     for pkg in packages:
        #         try:
        #             version = pkg_resources.get_distribution(pkg).version
        #             installed_packages[category].append((pkg, version))
        #         except pkg_resources.DistributionNotFound:
        #             pass

        installed_packages = {}

        for category, packages in package_mapping.items():
            installed_packages[category] = []
            for pkg in packages:
                try:
                    version = importlib.metadata.version(pkg)
                    installed_packages[category].append((pkg, version))
                except importlib.metadata.PackageNotFoundError:
                    pass

        return installed_packages

async def main(hook_id='79a979882bc330f25b0e785eb13360be'):
    vnstock_initializer = VnstockInitializer(hook_id)
    await vnstock_initializer.check_terms_accepted()

# # Run the event loop
asyncio.run(main())