{
    'name': 'Hide lots out of stock',
    'version': '1.0',
    'description': 'Hide lots out of stock',
    'summary': 'When a lot is out of stock, it is hidden from the list of lots in sale order lines',
    'author': 'Soy Calidad',
    'website': 'https://www.soycalidad.com',
    'license': 'Other proprietary',
    'category': 'stock',
    'depends': [
        'account',
        'stock',
    ],
    'data': [
        'views/stock.xml',
    ],
    'auto_install': False,
    'application': False,
}