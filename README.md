# Pegasoft Backend API Projesi

Flask ile geliştirilmiş kullanıcı yönetimi API'si. 
JWT ile login sistemi, kullanıcı ekleme, listeleme ve silme işlemleri yapılabilir.

## 🚀 Özellikler
- Kullanıcı Ekle (POST)
- Login (JWT Token)
- Kullanıcı Listeleme (GET - Token Gerektirir)
- Kullanıcı Silme (DELETE)

## 📸 API Testleri (Postman)
Aşağıda Postman ile yapılan testlerin ekran görüntüleri bulunmaktadır.

### Kullanıcı Ekleme
![Add User](screenshots/add_user.png)

### Login İşlemi
![Login](screenshots/login.png)

### Kullanıcı Listeleme
![Get Users](screenshots/get_users.png)

### Kullanıcı Silme
![Delete User](screenshots/delete_user.png)

## ⚙️ Kurulum
```bash
pip install -r requirements.txt
python app.py
