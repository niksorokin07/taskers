from werkzeug.security import check_password_hash, generate_password_hash
print(check_password_hash("pbkdf2:sha256:260000$iO6n7RzjsLtNUCXP$d23c0fe6263f16b80486cbf5258551677008de96b0fa7458b3a2bf55d3ec4f92", "12345"))