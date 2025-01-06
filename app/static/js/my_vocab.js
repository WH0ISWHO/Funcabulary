class Vocabulary {
    constructor() {
        this.wordInput = document.querySelector('#word');
        this.meaningInput = document.querySelector('#meaning');
        this.wordList = document.querySelector('#wordList');
        this.addBtn = document.querySelector('#add');
        this.removeBtn = document.querySelector('#remove-all');
        this.saveBtn = document.querySelector('#save-words');

        this.initialize();
    }

    initialize() {
        this.addBtn.addEventListener("click", () => this.add());
        this.removeBtn.addEventListener("click", () => this.remove());
        this.saveBtn.addEventListener("click", () => this.save());
    }

    add() {
        const word = this.wordInput.value.trim();
        const meaning = this.meaningInput.value.trim();

        if (word && meaning) {
            // create list item to hold the card
            const li = document.createElement('li');
            li.className = 'word-item';

            // create card element
            const card = document.createElement('div');
            card.className = 'card';

            // create front and back of the card
            const cardFront = document.createElement('div');
            cardFront.className = 'card-face card-front';
            cardFront.textContent = word;

            const cardBack = document.createElement('div');
            cardBack.className = 'card-face card-back';
            cardBack.textContent = meaning;

            // create Remove button
            const removeBtn = document.createElement('button');
            removeBtn.textContent = 'Remove';
            removeBtn.className = 'remove-btn';
            removeBtn.addEventListener('click', () => li.remove());

            // append card faces to the card
            card.appendChild(cardFront);
            card.appendChild(cardBack);

            // append card and remove button to list item
            li.appendChild(card);
            li.appendChild(removeBtn);

            // append list item to word list
            this.wordList.appendChild(li);

            // add flip functionality to card
            card.addEventListener('click', function () {
                card.classList.toggle('flipped');
            });

            // reset input fields
            this.wordInput.value = '';
            this.meaningInput.value = '';

            this.wordInput.focus();
        } else {
            alert("You must enter both a word and its meaning.");
        }
    }

    remove(){
        while(this.wordList.firstChild){
            this.wordList.removeChild(this.wordList.firstChild);
        }

        this.wordInput.value = '';
        this.meaningInput.value = '';
        this.wordInput.focus();
    }

    save() {
        const wordItems = document.querySelectorAll('.word-item');
        const wordsData = [];

        // extract words and meanings from the word list
        wordItems.forEach(item => {
            const word = item.querySelector('.card-front').textContent;
            const meaning = item.querySelector('.card-back').textContent;
            wordsData.push(`${word}: ${meaning}`);
        });

        // create a file and download it
        const blob = new Blob([wordsData.join('\n')], { type: 'text/plain' });
        const a = document.createElement('a');
        const url = URL.createObjectURL(blob);
        a.href = url;
        a.download = 'wordList.txt';
        a.click();

        URL.revokeObjectURL(url);
    }
}

// start the Vocabulary app
const vocabularyApp = new Vocabulary();