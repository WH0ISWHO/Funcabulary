document.querySelectorAll('.cards-container').forEach(container => {
    container.addEventListener('click', function() {
        document.querySelectorAll('.cards-container.flipped').forEach(card => {
            if(card !== this){
                card.classList.remove('flipped');
            }
        });

        this.classList.toggle('flipped');
    });
});

function Pronunciation(word, event){
    event.stopPropagation();
    fetch(`/tts?word=${word}`).then(response => response.json()).then(data => {
        if(data.audio_url){
            const audio = document.getElementById("player");
            audio.src = data.audio_url;
            audio.play();
        }else{
            alert("TTS audio is not available!");
        }
    })
    .catch(error => console.error("TTS Error:", error));
}