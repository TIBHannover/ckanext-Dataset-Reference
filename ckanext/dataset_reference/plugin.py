import ckan.plugins as plugins
import ckan.plugins.toolkit as toolkit
from flask import Blueprint
from ckanext.dataset_reference.controllers.link_reference import LinkReferenceController


class DatasetReferencePlugin(plugins.SingletonPlugin):
    plugins.implements(plugins.IConfigurer)
    plugins.implements(plugins.IBlueprint)
    

    def update_config(self, config_):
        toolkit.add_template_directory(config_, 'templates')
        toolkit.add_public_directory(config_, 'public')       
        toolkit.add_resource('public/statics', 'ckanext-dataset-reference')
    

    def get_blueprint(self):

        blueprint = Blueprint(self.name, self.__module__)        
       
        blueprint.add_url_rule(
            u'/dataset_reference/save_doi',
            u'save_doi',
            LinkReferenceController.save_doi,
            methods=['POST']
            )
        
        blueprint.add_url_rule(
            u'/dataset_reference/get_publication/<name>',
            u'get_publication',
            LinkReferenceController.get_publication,
            methods=['GET']
        )

        blueprint.add_url_rule(
            u'/dataset_reference/doi_is_valid',
            u'doi_is_valid',
            LinkReferenceController.doi_is_valid,
            methods=['POST']
        )

        blueprint.add_url_rule(
            u'/dataset_reference/delete_doi/<doi_id>',
            u'delete_doi',
            LinkReferenceController.delete_doi,
            methods=['GET']
        )

        blueprint.add_url_rule(
            u'/dataset_reference/add_publication_manually/<package_name>',
            u'add_publication_manually',
            LinkReferenceController.add_publication_manually,
            methods=['GET']
        )

        blueprint.add_url_rule(
            u'/dataset_reference/save_publication_manually',
            u'save_publication_manually',
            LinkReferenceController.save_publication_manually,
            methods=['POST']
        )

        return blueprint
