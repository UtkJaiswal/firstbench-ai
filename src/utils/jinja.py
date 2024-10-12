from pathlib import Path
from jinja2 import Environment, FileSystemLoader, StrictUndefined, TemplateError
import frontmatter
from jinja2 import meta

class PromptManager:
    _env = None  

    @classmethod
    def _get_env(self, templates_dir="prompts"):
        """Initializes and caches the Jinja2 Environment for template loading."""
        templates_dir = Path(__file__).parent.parent.parent / templates_dir
        if self._env is None:
            self._env = Environment(
                loader=FileSystemLoader(templates_dir), 
                undefined=StrictUndefined 
            )
        return self._env

    @staticmethod
    def get_prompt(template, **kwargs):
        """Loads and renders a template with the provided kwargs."""
        env = PromptManager._get_env()
        template_path = f"{template}.j2"

        try:
            with open(env.loader.get_source(env, template_path)[1]) as file:
                post = frontmatter.load(file)
                
                template = env.from_string(post.content)
                
                a=template.render(**kwargs)
                return a
        except TemplateError as e:
            raise ValueError(f"Error rendering template: {str(e)}")

    @staticmethod
    def get_template_info(template):
        """Retrieves metadata and variables from the template."""
        env = PromptManager._get_env()
        template_path = f"{template}.j2"

        try:
            with open(env.loader.get_source(env, template_path)[1]) as file:
                post = frontmatter.load(file)
                ast = env.parse(post.content)
                variables = meta.find_undeclared_variables(ast)

                return {
                    "name": template,
                    "description": post.metadata.get("description", "No description provided"),
                    "author": post.metadata.get("author", "Unknown"),
                    "variables": list(variables),
                    "frontmatter": post.metadata
                }
        except Exception as e:
            raise ValueError(f"Error loading template info: {str(e)}")