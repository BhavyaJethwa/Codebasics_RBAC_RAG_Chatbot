# # Loading documents by role

# def load_documents_by_role(role: str):
#     base_path = "./resources/data"
#     role_paths = {
#         "finance": ["finance"],
#         "marketing": ["marketing"],
#         "engineering": ["engineering"],
#         "human_resource": ["hr"],
#         "employee": ["general"],
#     }

#     folders = role_paths.get(role, ["general"])
#     print("folders: ", folders)
#     docs = []

#     for folder in folders:
#         path = os.path.join(base_path, folder)
#         print("path: ", path)
#         if os.path.exists(path):
#             for file_name in os.listdir(path):
#                 file_path = os.path.join(path, file_name)
#                 print("file_path:", file_path)

#                 try:
#                     loaded_docs = []
#                     if file_name.endswith(".csv"):
#                         loaded_docs = load_csv(file_path)
#                         print(file_name, "CSV Documents loaded :" , file_path)
#                         print("Number of Documents loaded: ",len(loaded_docs))
#                         print("------------------------------------------------------------------------------------------------------------")

#                     elif file_name.endswith(".md"):
#                         loaded_docs = load_markdown(file_path)
#                         print(file_name, "MD Documents loaded", file_path)
#                         print("Number of Documents loaded: ",len(loaded_docs))
#                         print("------------------------------------------------------------------------------------------------------------")

#                     elif file_name.endswith(".txt"):
#                         loaded_docs = load_text(file_path)
#                         print(file_name,"Text Documents loaded", file_path)

#                     elif file_name.endswith(".pdf"):
#                         loaded_docs = load_pdf(file_path)
#                         print(file_name,"PDF Documents loaded", file_path)

#                     elif file_name.endswith(".docx"):
#                         loaded_docs = load_docx(file_path)
#                         print(file_name,"Word Documents loaded", file_path)

#                     else:
#                         continue

#                     # Add metadata
#                     for doc in loaded_docs:
#                         doc.metadata["source"] = file_path
#                         doc.metadata["role"] = folder
#                         doc.metadata["last_modified"] = datetime.fromtimestamp(os.path.getmtime(file_path)).strftime('%Y-%m-%d %H:%M:%S')

#                     docs.extend(loaded_docs)

#                 except Exception as e:
#                     print(f"Failed to load {file_path}: {e}")
#     print("Total docs loaded : ",len(docs))
#     return docs

# roles = ["finance", "human_resource", "marketing", "engineering", "employee"]
# def get_documents_by_role():
#     documents_by_role = {}
#     for role in roles:
#         print("===============================================================================================================")
#         print(f"Loading document for {role} ...... ")
#         documents_by_role[role] = load_documents_by_role(role)
#         print(f"Loading document for {role} complete")
#     return documents_by_role    
    
# role_documents = get_documents_by_role()

# #------------------------------------------------------------------------------------------------------------------------------------------------

# for role , docs in role_documents.items():
#     print(role.upper(), ":-")
#     print("Total Documents passed: ",len(docs))
#     create_vector_store(docs=docs, collection_name=role)

# def create_retriever_by_role(role):
#    return Chroma(persist_directory=persist_directory, 
#                         embedding_function=embedding, 
#                         collection_name = role).as_retriever()

# def get_retriever_by_role():
#     retrievers = {}
#     for role in role_documents.keys():
#         print(f"Creating retriever for role: {role}...")
#         retrievers[role] = create_retriever_by_role(role)
#         print(f"Creating retriever for role: {role} success")
#     return retrievers

# retrievers_by_roles = get_retriever_by_role()









# def load_documents_by_role(role: str):
#     base_path = "resources/data"
#     role_paths = {
#         "finance": ["finance"],
#         "marketing": ["marketing"],
#         "engineering": ["engineering"],
#         "human_resource": ["hr"],
#         "employee": ["general"]
#     }

#     folders = role_paths.get(role, ["general"])
#     print("folders: ", folders, "for role: ", role)
#     docs = []
#     for folder in folders:
#         path = os.path.join(base_path, folder)
#         print("path: ", path)
#         if os.path.exists(path):
#             for file_name in os.listdir(path):
#                 file_path = os.path.join(path, file_name)
#                 print("file_path:", file_path)

#                 try:
#                     loaded_docs = []
#                     if file_name.endswith(".csv"):
#                         loaded_docs = load_csv(file_path)
#                         print(file_name, "CSV Documents loaded :" , file_path)
#                         print("Number of Documents loaded: ",len(loaded_docs))
#                         print("------------------------------------------------------------------------------------------------------------")
        
#                     elif file_name.endswith(".md"):
#                         loaded_docs = load_markdown(file_path)
#                         print(file_name, "MD Documents loaded", file_path)
#                         print("Number of Documents loaded: ",len(loaded_docs))
#                         print("------------------------------------------------------------------------------------------------------------")

#                     elif file_name.endswith(".txt"):
#                         loaded_docs = load_text(file_path)
#                         print(file_name,"Text Documents loaded", file_path)

#                     elif file_name.endswith(".pdf"):
#                         loaded_docs = load_pdf(file_path)
#                         print(file_name,"PDF Documents loaded", file_path)

#                     elif file_name.endswith(".docx"):
#                         loaded_docs = load_docx(file_path)
#                         print(file_name,"Word Documents loaded", file_path)

#                     else:
#                         continue
                    
#                     for doc in loaded_docs:
#                         doc.metadata["source"] = file_path
#                         doc.metadata["role"] = folder

#                     docs.extend(loaded_docs)
#                 except Exception as e:
#                     print(f"Failed to load {file_path}: {e}")
#     print("Total docs loaded : ",len(docs))
#     return docs