{
    'name': 'Reporte PLE',
    'version': '1.0',
    'description': 'Generador PLE',
    'summary': 'Genera Reportes PLE de los distintos libros contables',
    'author': 'Luis Vargas',
    'website': '',
    'license': '',
    'category': '',
    'depends': [
        'account',
    ],
    'data': [ 'security/ir.model.access.csv',
        'views/generic_ple_views.xml'
    ],
    'demo': [
    ],
    'auto_install': True,
    'application': True,
}