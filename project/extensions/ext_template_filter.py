
def init_app(app):

    # Define template filter
    @app.template_filter('document_status')
    def document_status_filter(value):
        status_map = {
            'init': ('Initialized', 'bg-blue-200 text-blue-600'),
            'indexing': ('Indexed', 'bg-orange-200 text-orange-600'),
            'error': ('Error', 'bg-red-200 text-red-600'),
            'completed': ('Completed', 'bg-green-200 text-green-600')
        }
        return status_map.get(value, ('Unknown Status', 'bg-gray-200 text-gray-600'))


