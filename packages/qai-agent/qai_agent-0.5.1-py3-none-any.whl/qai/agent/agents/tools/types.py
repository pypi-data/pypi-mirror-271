# from llama_index.core.tools.types import ToolMetadata as LLamaToolMetadata


# class ToolMetadata(LLamaToolMetadata):
#     """ Enhanced Tool metadata that can work with enums and properties.
#     """
#     def _is_object(self, d: dict) -> bool:
#         """Check if the dict is an object."""
#         return d.get("type") == "object"

#     def _update_object(self, d: dict) -> dict:
#         """
#         Recursively update the object properties,
#         will change referenced types to their actual properties.
#         Additionally for enums, will add the enum values to the properties as expected with openai.
#         Fields that named _<field>_properties will be added to the field properties.
#         Args:
#             d (dict): The object properties dict
#         Returns:
#             dict: The updated object properties dict
#         """
#         nd = {}
#         k: str
#         v: dict
#         schema = self.fn_schema.schema()
#         referenced_types = schema.get("$defs", {})

#         for k, v in d.items():
#             if self._is_object(v):
#                 nd[k] = self._update_object(v["properties"])
#                 continue
#             ## get any additional properties for the field
#             props = getattr(self.fn_schema, f"_{k}_properties", None)
#             if props:
#                 props = dict(props.default)

#             if referenced_types and "$ref" in v:
#                 typ = v.pop("$ref").split("/")[-1]  ## e.g. #/$defs/<type>
#                 if typ in referenced_types:
#                     ref_typ = referenced_types[typ]
#                     v = {
#                         k2: v2
#                         for k2, v2 in ref_typ.items()
#                         if k2 in ["type", "enum", "properties", "required", "definitions"]
#                     }
#             if props:
#                 v.update(props)

#             nd[k] = v
#         return nd

#     def get_parameters_dict(self) -> dict:
#         d = super().get_parameters_dict()
#         ## Recursively update the parameters dict for every "type" : "object"
#         if self._is_object(d):
#             d["properties"] = self._update_object(d["properties"])
#         # from pprint import pprint
#         # print(f"#############")
#         # pprint(d)
#         # print(f"#############")
#         return d
