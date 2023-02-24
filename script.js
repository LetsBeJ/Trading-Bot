window.onload = function() {
	var navLinks = document.querySelectorAll('nav a');
	
	for (var i = 0; i < navLinks.length; i++) {
		navLinks[i].addEventListener('click', function(e) {
			e.preventDefault();
			var sectionId = this.getAttribute('href').substr(1);
			var section = document.getElementById(sectionId);
			section.scrollIntoView({ behavior: 'smooth' });
		});
	}
};
