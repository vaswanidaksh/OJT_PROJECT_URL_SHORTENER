 function showSection(section) {
            document.getElementById('main').classList.add('hidden');
            document.getElementById('about').classList.add('hidden');
            document.getElementById(section).classList.remove('hidden');
        }