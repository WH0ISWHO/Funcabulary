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



function Pronunciation_eng(word, language, event) {
    event.stopPropagation();
    fetch(`/tts_eng?word=${word}&lang=${language}`)
        .then(response => response.json())
        .then(data => {
            const audio = document.getElementById("player_eng");
            
            if (language === "eng" && data.eng_audio_url) {
                audio.src = data.eng_audio_url;
                audio.play();
            } else {
                alert("Audio is not available for this language!");
            }
        })
        .catch(error => console.error("TTS Error:", error));
}



function Pronunciation_kor(meaning, language, event) {
    event.stopPropagation();

    const encodedMeaning = encodeURIComponent(meaning);

    fetch(`/tts_kor?meaning=${encodedMeaning}&lang=${language}`)
        .then(response => response.json())
        .then(data => {
            const audio = document.getElementById("player_kor");

            if (data.kor_audio_urls && data.kor_audio_urls.length > 0) {
                audio.src = data.kor_audio_urls[0];
                audio.play();
            } else {
                alert("Audio is not available for this language!");
            }
        })
        .catch(error => console.error("TTS Error:", error));
}
