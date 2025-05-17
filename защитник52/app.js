var menuButton = document.querySelector('.menu-button');
var menu = document.querySelector('.list_of_items');
menuButton.addEventListener('click', function () {
    menuButton.classList.toggle('menu-button-active');
    menu.classList.toggle('active');
})







const phoneNumbers = [
  "+7 (981) 274-79-19",
  "+7 (981) 248-84-94"
];

function getDailyPhoneNumber() {
  const now = new Date();
  const start = new Date(now.getFullYear(), 0, 0);
  const diff = now - start;
  const oneDay = 1000 * 60 * 60 * 24;
  const dayOfYear = Math.floor(diff / oneDay);
  
  return phoneNumbers[dayOfYear % phoneNumbers.length];
}

document.addEventListener('DOMContentLoaded', function() {
  document.getElementById('rotatingPhoneNumber').textContent = getDailyPhoneNumber();
  
  setInterval(function() {
      document.getElementById('rotatingPhoneNumber').textContent = getDailyPhoneNumber();
  }, 300000);
});

function getDailyPhoneNumber() {
  const now = new Date();
  const start = new Date(now.getFullYear(), 0, 0);
  const diff = now - start;
  const oneDay = 1000 * 60 * 60 * 24;
  const dayOfYear = Math.floor(diff / oneDay);
  
  return phoneNumbers[dayOfYear % phoneNumbers.length];
}

document.addEventListener('DOMContentLoaded', function() {
  document.getElementById('rotatingPhone').textContent = getDailyPhoneNumber();
  
  setInterval(function() {
      document.getElementById('rotatingPhone').textContent = getDailyPhoneNumber();
  }, 300000);
});

function getDailyPhoneNumber() {
  const now = new Date();
  const start = new Date(now.getFullYear(), 0, 0);
  const diff = now - start;
  const oneDay = 1000 * 60 * 60 * 24;
  const dayOfYear = Math.floor(diff / oneDay);
  
  return phoneNumbers[dayOfYear % phoneNumbers.length];
}

document.addEventListener('DOMContentLoaded', function() {
  document.getElementById('rotatingPhone').textContent = getDailyPhoneNumber();
  
  setInterval(function() {
      document.getElementById('rotatingPhoneNumberSvaz').textContent = getDailyPhoneNumber();
  }, 300000);
});








document.addEventListener('DOMContentLoaded', function() {
    const tabButtons = document.querySelectorAll('.tab-button');
    const tabPanes = document.querySelectorAll('.tab-pane');
    
    tabButtons.forEach(button => {
      button.addEventListener('click', function() {
        tabButtons.forEach(btn => btn.classList.remove('active'));
        tabPanes.forEach(pane => pane.classList.remove('active'));
        
        this.classList.add('active');
        
        const tabName = this.getAttribute('data-tab');
        const activePane = document.querySelector(`[data-tab-content="${tabName}"]`);
        if (activePane) {
          activePane.classList.add('active');
          activePane.removeAttribute('hidden');
        }
        
        tabPanes.forEach(pane => {
          if (!pane.classList.contains('active')) {
            pane.setAttribute('hidden', '');
          }
        });
      });
    });
  });

  document.addEventListener('DOMContentLoaded', function() {
    const tracks = document.querySelectorAll('.slider-track');
    const dots = document.querySelectorAll('.dot');
    const prevBtns = document.querySelectorAll('.prev');
    const nextBtns = document.querySelectorAll('.next');
    let currentSlide = 0;
    let slideInterval;
    const slideDuration = 10000;
    
    function showSlide(index) {
      tracks.forEach(track => track.classList.remove('active'));
      dots.forEach(dot => dot.classList.remove('active'));
      
      tracks[index].classList.add('active');
      dots[index].classList.add('active');
      currentSlide = index;
    }
    
    function nextSlide() {
      let newIndex = (currentSlide + 1) % tracks.length;
      showSlide(newIndex);
    }
    
    function prevSlide() {
      let newIndex = (currentSlide - 1 + tracks.length) % tracks.length;
      showSlide(newIndex);
    }
    
    function startAutoPlay() {
      slideInterval = setInterval(nextSlide, slideDuration);
    }
    
    function stopAutoPlay() {
      clearInterval(slideInterval);
    }

    nextBtns.forEach(btn => {
      btn.addEventListener('click', function(e) {
        e.stopPropagation();
        nextSlide();
        stopAutoPlay();
        startAutoPlay();
      });
    });
    
    prevBtns.forEach(btn => {
      btn.addEventListener('click', function(e) {
        e.stopPropagation();
        prevSlide();
        stopAutoPlay();
        startAutoPlay();
      });
    });
    
    dots.forEach((dot, index) => {
      dot.addEventListener('click', function() {
        showSlide(index);
        stopAutoPlay();
        startAutoPlay();
      });
    });
    
    const slider = document.querySelector('.slider-container');
    slider.addEventListener('mouseenter', stopAutoPlay);
    slider.addEventListener('mouseleave', startAutoPlay);
    
    showSlide(0);
    startAutoPlay();
  });

  document.addEventListener('DOMContentLoaded', function() {
    const questions = document.querySelectorAll('.faq-question');
    
    questions.forEach(question => {
      question.addEventListener('click', () => {
        const item = question.parentNode;
        const answer = question.nextElementSibling;
        const isOpen = item.classList.contains('active');
        
        document.querySelectorAll('.faq-item').forEach(el => {
          el.classList.remove('active');
          el.querySelector('.faq-answer').style.maxHeight = null;
          el.querySelector('.faq-question').classList.remove('active');
        });
        
        if (!isOpen) {
          item.classList.add('active');
          question.classList.add('active');
          answer.style.maxHeight = answer.scrollHeight + 'px';
        }
      });
    });
    
    const firstQuestion = document.querySelector('.faq-question');
    if (firstQuestion) {
      firstQuestion.click();
    }
  });


  document.addEventListener('DOMContentLoaded', function() {
    const burgerButton = document.getElementById('burgerButton');
    const menuItems = document.getElementById('menuItems');
    
    burgerButton.addEventListener('click', function() {
        this.classList.toggle('active');
        menuItems.classList.toggle('active');
        
        if (menuItems.classList.contains('active')) {
            document.body.style.overflow = 'hidden';
        } else {
            document.body.style.overflow = '';
        }
    });
    
    document.querySelectorAll('.item').forEach(item => {
        item.addEventListener('click', function() {
            if (window.innerWidth <= 992) {
                burgerButton.classList.remove('active');
                menuItems.classList.remove('active');
                document.body.style.overflow = '';
            }
        });
    });
});

document.getElementById('candidateForm').addEventListener('submit', function(e) {
  e.preventDefault();
  const form = e.target;
  const submitBtn = form.querySelector('button[type="submit"]');
  
  submitBtn.textContent = 'Отправка...';
  submitBtn.disabled = true;
  
  fetch(form.action, {
    method: 'POST',
    body: new FormData(form),
    headers: {
      'Accept': 'application/json'
    }
  })
  .then(response => {
    if (response.ok) {
      alert('Анкета успешно отправлена! Мы свяжемся с вами по WhatsApp.');
      form.reset();
    } else {
      throw new Error('Ошибка отправки формы');
    }
  })
  .catch(error => {
    alert('Произошла ошибка. Пожалуйста, попробуйте еще раз.');
    console.error(error);
  })
  .finally(() => {
    submitBtn.textContent = 'Отправить анкету';
    submitBtn.disabled = false;
  });
});