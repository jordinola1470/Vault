async function sendInput(){

    // Obtener el input en el area de texto

    const promptTexto = document.getElementById('textarea_prompt').value
    
    // Mensaja de espera de resultados

    const listsResponses = ['#response_openai', '#response_deepseek', '#response_claude'];
  
    listsResponses.forEach(responses => {
        const reponseBox = document.querySelector(`${responses}.responses-contenido`);
        if (reponseBox){
            reponseBox.innerHTML = "<em> Esperando Respuestas<em>"
        }

    });

    try{
        const response = await fetch('http://localhost:9999/api/fake',// Cambiar por le local del backend
            {
                method: 'POST',
                headers:{'Content-Type' : 'application/json'},
                body: JSON.stringify({prompt: promptTexto})
            }
        )

        const data = await response.json();

        const html_openai = marked.parse(data.openai);

    
        document.getElementById('contenido_openai').innerHTML = html_openai

    } 
    
    catch (e) {
        
        console.error('Error al enviar el prompt al backend',e)
        

        // listsResponses.forEach(responses => {
        //     document.querySelector(`${responses} p`).textContent = "Sin Respuesta";
        // })

    }

};