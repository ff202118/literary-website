from werkzeug.security import generate_password_hash
 
# 生成密码
hash = generate_password_hash('pbkdf2:sha256:260000$QQdVfy8rTZOnKthJ$79ef31fdb92d0588bc2367b3a8c7a04b38355ad914207cd74e98dd6ff108454d')
print(hash)