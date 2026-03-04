import requests
import json
import gradio as gr

url="http://localhost:11434/api/generate"

headers={
    'Content-Type':'application/json'
}
history=[]
def generate_response(prompt):
    history.append(prompt)
    finalprompt="\n".join(history)
    data={
        "model":"codellama-another",
        "prompt":finalprompt,
        "stream":False,
    }

    response=requests.post(url,headers=headers,data=json.dumps(data))

    if response.status_code==200:
        response=response.text
        data=json.loads(response)
        actualresponse=data['response']
        return actualresponse
    else:
        print("error",response.text)


interface=gr.Interface(
    fn=generate_response,
    inputs=gr.Textbox(lines=3,placeholder="Enter your prompt"),
    outputs="text",
)
interface.launch()