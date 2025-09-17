from odoo import api,SUPERUSER_ID

def test_post_init_hook(cr,registry):
    env = api.Environment(cr,SUPERUSER_ID,{})
    env.cr.execute("update account_journal set short_name=name where type in ('cash','bank')")