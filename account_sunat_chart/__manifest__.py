{
    'name': 'Catálogos SUNAT',
    'version': '1.0',
    'description': 'Catálogos de SUNAT',
    'summary': 'Añade los catálogos del 1 a la 35 proporcionadas por SUNAT',
    'author': 'Soy Calidad',
    'website': '',
    'license': 'LGPL-3',
    'category': '',
    'depends': [
        'account',
    ],
    'data': [ 
        'security/ir.model.access.csv',
        'data/charts_data.xml'
    ],
    'auto_install': True,
    'application': True,
}