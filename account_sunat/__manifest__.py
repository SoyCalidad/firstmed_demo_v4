{
    'name': 'Asientos Contables SUNAT',
    'version': '1.0',
    'description': 'Añade campos para las cuentas contables a SUNAT',
    'summary': 'Añade Campos y funcionalidad para adecuar los asientos contables',
    'author': 'Soy Calidad',
    'website': 'www.soycalidad.com',
    'license': 'Other proprietary',
    'category': 'account',
    'depends': [
        'account_sunat_chart'
    ],
    'data': [ 
        'security/ir.model.access.csv',
        'data/account_categories.xml',
        'views/views.xml',
        'views/menus.xml',
    ],
    'auto_install': True,
    'application': True,
}