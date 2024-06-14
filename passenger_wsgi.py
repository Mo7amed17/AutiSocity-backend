import sys
import os

# تحديد المسار للجذر الرئيسي للتطبيق
app_root = '/home/origmtie/autisociety-api.original-business.com'
sys.path.insert(0, app_root)

# تفعيل البيئة الافتراضية
venv_path = '/home/origmtie/virtualenv/autisociety-api.original-business.com/3.9'
activate_env = os.path.join(venv_path, 'bin/activate_this.py')
exec(open(activate_env).read(), {'__file__': activate_env})

# استيراد التطبيق
from application import app as application