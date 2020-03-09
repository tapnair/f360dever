find_attributes_help_text = """
Find attributes attached to objects in this product that match the group and or attribute name. This does not find 
attributes attached directly to the Product or Document objects but finds the attributes attached to entities within 
the product.\n<br><br>

The search string for both the groupName and attributeName arguments can be either an absolute name value, or a regular 
expression. With an absolute name, the search string must match the entire groupName or attributeName, including case. 
An empty string will match everything. For example if you have an attribute group named "MyStuff" that contains the 
attribute "Length1", using the search string "MyStuff" as the group name and "Length1" as the attribute name will 
find the attributes with those names. Searching for "MyStuff" as the group name and "" as the attribute name will 
find all attributes that have "MyStuff" as the group name.\n<br><br>

Regular expressions provide a more flexibile way of searching. To use a regular expression, prefix the input string 
for the groupName or attributeName arguments with "re:". The regular expression much match the entire group or 
attribute name. For example if you have a group that contains attributes named "Length1", "Length2", "Width1", 
and "Width2" and want to find any of the length attributes you can use a regular expression using the string 
"re:Length.*". For more information on attributes see the Attributes topic in the user manual.\n<br><br>
"""
