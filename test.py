import google.generativeai as genai

genai.configure(api_key="AIzaSyCNdCVHytAlQgfWIUQ4Q_l_2d8XVH-kzTU")

for m in genai.list_models():
    print(m.name)
