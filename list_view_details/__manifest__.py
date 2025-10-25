{
    "name": "Record Details In List View",
    "summary": "Show record details in list view without opening the form view",
    "author": "Mihran Thalhath",
    "website": "https://github.com/MihranThalhath",
    "license": "AGPL-3",
    "category": "Uncategorized",
    "version": "19.0.1.0.0",
    "depends": ["web"],
    "data": [
        "security/ir.model.access.csv",
        "views/list_view_details.xml",
        "data/data.xml",
    ],
    "assets": {
        "web.assets_backend": [
            "list_view_details/static/src/**/*.xml",
            "list_view_details/static/src/**/*.js",
        ],
    },
    "images": ["static/description/images/list_view_details.png"],
    "uninstall_hook": "uninstall_hook",
}
