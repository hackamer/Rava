# Rava Desktop Application / نرم‌افزار دسکتاپ Rava

\[TOC]

این فایل `README.md` به صورت دوزبانه (فارسی و انگلیسی) طراحی شده و شامل لینک‌ها برای دسترسی سریع به بخش‌ها است.

---
## نمای فعلی نرم افزار/Preview of App

![image](preview.png)

## معرفی / Introduction

### فارسی

Rava یک نرم‌افزار گزارش‌دهی پرستاری الکترونیکی است که به حذف استفاده از کاغذ و صرفه‌جویی در زمان پرستاران کمک می‌کند. این نرم‌افزار برای ثبت داده‌های بیماران و کاربران طراحی شده و امنیت بالایی دارد.

### English

Rava is an electronic nursing reporting software that helps eliminate paper usage and save nurses' time. It is designed to record patient and user data while providing high-level security.

---

## ویژگی‌ها / Features

### فارسی

* ورود و ثبت‌نام امن با هش کردن رمز عبور.
* نقش‌ها و مجوزهای کاربری (ادمین و کاربران عادی).
* مدیریت و جستجوی گزارش‌های بیماران.
* مدیریت داروها با زمان‌بندی مصرف.
* رمزگذاری داده‌ها و اعتبارسنجی مبتنی بر شناسه سخت‌افزار.
* اعلان‌های بلادرنگ در داخل برنامه.

### English

* Secure login and signup with password hashing.
* User roles and permissions (admin and standard users).
* Patient report management and search functionality.
* Medicine entry management with time tracking.
* Data encryption and verification tied to hardware ID.
* Real-time notifications within the application.

---

## نصب / Installation

### فارسی

### پیش‌نیازها

* Python 3
* PyQt5
* bcrypt
* cryptography
* jdatetime
* unidecode

### English

### Requirements

* Python 3
* PyQt5
* bcrypt
* cryptography
* jdatetime
* unidecode

### فارسی

### استفاده از venv برای محیط مجازی

1. ترمینال یا CMD را باز کنید.
2. به مسیر پروژه بروید:

```bash
cd path/to/rava
```

3. ایجاد یک محیط مجازی:

```bash
python -m venv venv
```

4. فعال‌سازی محیط مجازی:

* **ویندوز:** `venv\Scripts\activate`
* **لینوکس/macOS:** `source venv/bin/activate`

5. نصب بسته‌های مورد نیاز:

```bash
pip install -r requirements.txt
```

> اگر `requirements.txt` موجود نیست، می‌توانید به‌صورت دستی نصب کنید:

```bash
pip install PyQt5 bcrypt cryptography jdatetime unidecode
```

### English

### Using `venv` for a virtual environment

1. Open a terminal or command prompt.
2. Navigate to the project directory:

```bash
cd path/to/rava
```

3. Create a virtual environment:

```bash
python -m venv venv
```

4. Activate the virtual environment:

* **Windows:** `venv\Scripts\activate`
* **Linux/macOS:** `source venv/bin/activate`

5. Install required packages:

```bash
pip install -r requirements.txt
```

> If `requirements.txt` is not available, you can manually install:

```bash
pip install PyQt5 bcrypt cryptography jdatetime unidecode
```

---

## اجرای Rava / Running Rava

### فارسی

```bash
python main.py
```
و یا 

```bash
python full.py
```
پنجره ورود ظاهر می‌شود. از مشخصات پیش‌فرض ادمین برای ایجاد کاربران و مدیریت گزارش‌ها استفاده کنید:

* **نام کاربری:** admin
* **رمز عبور:** P\@ssw0rd

### English

```bash
python main.py
```

or

```bash
python full.py
```

The login window will appear. Use the default admin credentials to create users and start managing reports:

* **Username:** admin
* **Password:** P\@ssw0rd

---

## ساختار پروژه / Project Structure

### فارسی

* `main.py`: کد اصلی برنامه.
* `notification.py`: کد تنظیم اعلان‌ها.
* `imports.py`: همه ماژول‌های import در این فایل.
* `encryption.py`: کدهای رمزگذاری و رمزگشایی فایل‌ها.
* `config.py`: مقادیر پایه و مهم.
* `database.py`: کد تغییرات دیتابیس.
* `full.py`: کد کامل برنامه بدون وابستگی.

* `ui/`: پوشه حاوی فایل‌های UI با فرمت `.ui`.
* `images/`: آیکون‌ها و لوگوهای برنامه.
* `ui/fonts/`: فونت‌های استفاده‌شده در برنامه.
* `AppData/Local/Rava/`: محل پیش‌فرض ذخیره‌سازی داده‌ها و فایل‌های پیکربندی رمزگذاری‌شده.

### English

* `main.py`: Main application code.
* `notification.py`: Notification settings code.
* `imports.py`: All module imports in this file.
* `encryption.py`: Code for encrypting and decrypting files.
* `config.py`: Base and important values.
* `database.py`: Database modification code.
* `full.py`: full code with out need to here other codes.
* `ui/`: Directory containing PyQt5 UI `.ui` files.
* `images/`: Application icons and logos.
* `ui/fonts/`: Fonts used in the application.
* `AppData/Local/Rava/`: Default storage for encrypted data and config files.

---

## نکات / Notes

### فارسی

* اطمینان حاصل کنید سیستم شما اجازه ایجاد پوشه در `AppData/Local/` را دارد.
* گزارش‌ها رمزگذاری شده و با شناسه سخت‌افزار اعتبارسنجی می‌شوند.
* تنها کاربران ادمین می‌توانند سایر کاربران را ایجاد یا حذف کنند.

### English

* Ensure your system allows creating directories in `AppData/Local/` for proper storage.
* Reports are encrypted and verified using hardware ID to ensure integrity.
* Only admin users can create or delete other users.

---
 راوا  هدفش ارائه یک نرم‌افزار دسکتاپ امن، کاربرپسند و مدولار برای امور بهداشتی یا گزارش‌گیری اداری است.
 
Rava aims to provide a secure, intuitive, and modular desktop application for healthcare or administrative reporting tasks. 


