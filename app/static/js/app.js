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

// const cards = document.querySelectorAll(".word-card");
// const container = document.querySelector(".words-section");


// for(let card of cards){

//     const favorites = document.createElement('button');
//     favorites.classList.add('favoriteBtn');
//     favorites.textContent = '☆';
    

//     const fronts = card.querySelector('.front');
//     fronts.appendChild(favorites);

//     card.addEventListener('click', () =>{
//         for(let d of cards){
//             if(d !== card && d.classList.contains('flipped')){
//                 d.classList.remove('flipped');
//             }
//         }
//     card.classList.toggle('flipped');
//     });

//     favorites.addEventListener('click', (event) => {
//         event.stopPropagation();
//         favorites.classList.toggle('favorited');
//         if (favorites.classList.contains('favorited')) {
//             favorites.textContent = '★';
//             card.style.boxShadow='-1em 0 .1em rgb(243, 235, 5), 1em 0 .1em rgb(243, 235, 5)';
//         } else {
//             favorites.textContent = '☆';
//             card.style.boxShadow='';
//         }
//     });
// }
