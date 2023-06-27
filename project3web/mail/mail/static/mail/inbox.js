document.addEventListener('DOMContentLoaded', function() { 

  // Use buttons to toggle between views
  document.querySelector('#inbox').addEventListener('click', () => load_mailbox('inbox'));
  document.querySelector('#sent').addEventListener('click', () => load_mailbox('sent'));
  document.querySelector('#archived').addEventListener('click', () => load_mailbox('archive'));
  document.querySelector('#compose').addEventListener('click', compose_email);

  // By default, load the inbox
  load_mailbox('inbox');

  history.pushState({}, "", `inbox`)

  // select compose-form, add event listener for submit, run send_email function on submit
  document.querySelector('#compose-form').addEventListener('submit', send_email);    
});

function compose_email() {
  // Show compose view and hide other views
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'block';

  // Clear out composition fields
  document.querySelector('#compose-recipients').value = '';
  document.querySelector('#compose-subject').value = '';
  document.querySelector('#compose-body').value = '';

  // when user composes email, change url to reflect so
  history.pushState({}, "", `compose`)
}

function load_mailbox(mailbox) {
  // Show the mailbox and hide other views
  document.querySelector('#emails-view').style.display = 'block';
  document.querySelector('#compose-view').style.display = 'none';
 

  // Show the mailbox name  
  document.querySelector('#emails-view').innerHTML = `<h3>${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3>`;

  // get the desired contents for the 'inbox' mailbox 
  if (mailbox === 'inbox') {    
    fetch('/emails/inbox')
    .then(response => response.json())
    .then(emails => {       

      // cleans up url after the user replies or archives mail and then returns to a mailbox.
      if (window.location.pathname !== '/inbox') {
        history.replaceState({}, '', '/inbox');
      }

      // for every email, create a div, set its inner html to every individual email and add some styling to it
      emails.forEach(email => {
        const element = document.createElement('div');

        // set the div's id to later be able to select with querySelector
        element.id = email.id;
        element.style.border = '1px solid teal';
        element.innerHTML = `${email.sender} --- ${email.subject} --- ${email.timestamp}`;        
        element.style.margin = '2px';
        element.style.padding = '2px';

        // set background color of div depending on whether its 'read' property is true or false
        if (!email.read) {        
          element.style.backgroundColor = 'white';
        } else {        
          element.style.backgroundColor = 'gray';
        }

        // append email element with all its added styling to the DOM
        document.querySelector('#emails-view').append(element);
        
        element.addEventListener('click', () => {
          // when user clicks on an email, load contents of said mail
          view_email(element.id);
        });
      });
    })

    .catch(error => {
      console.log('Error:', error);
    });
  }

  // archived emails view
  if (mailbox === 'archive') {    
    fetch('/emails/archive')
    .then(response => response.json())
    .then(emails => {

      if (window.location.pathname !== '/archive') {
        history.replaceState({}, '', '/archive');
      }
      
      // each archived email gets its own div
      emails.forEach(email => {
        const archive_element = document.createElement('div');
        
        archive_element.id = email.id;
        archive_element.style.border = '1px solid teal';
        archive_element.innerHTML = `${email.sender} --- "${email.subject}" --- ${email.timestamp}`;        
        archive_element.style.margin = '2px';
        archive_element.style.padding = '2px';
        archive_element.style.backgroundColor = 'white';

        document.querySelector('#emails-view').append(archive_element);

        // when user clicks on an archived email, load contents of said mail
        archive_element.addEventListener('click', () => {          
          view_archived_email(archive_element.id);
        });
      });         
    });
  }

  // sent emails view
  if (mailbox === 'sent') {    
    fetch('/emails/sent')
    .then(response => response.json())
    .then(emails => {           

      if (window.location.pathname !== '/sent') {
        history.replaceState({}, '', '/sent');
      }

      // sent emails get their own individual div
      emails.forEach(email => {
        const sent_element = document.createElement('div');

        sent_element.id = email.id;
        sent_element.style.border = '1px solid teal';
        sent_element.innerHTML = `"${email.subject}" --- ${email.timestamp}`;        
        sent_element.style.margin = '3px';
        sent_element.style.padding = '2px';
        sent_element.style.backgroundColor = 'white';

        document.querySelector('#emails-view').append(sent_element);

        // when user clicks on an sent email, load contents of said mail
        sent_element.addEventListener('click', () => {          
          view_sent_email(sent_element.id);
        });
      });         
    });
  }
}

// prevent default form submission for one page app functionality
function send_email(event) {
  event.preventDefault();

  // form values that need to be saved inside the db
  const recipients = document.querySelector('#compose-recipients').value;
  const subject = document.querySelector('#compose-subject').value;
  const body = document.querySelector('#compose-body').value;

  // API request with email contents attached
  fetch('/emails', {
    method: 'POST',
    body: JSON.stringify({
      recipients: recipients,
      subject: subject,
      body: body
    })
  })

  .then(response => response.json())
  .then(result => {    
    console.log(result);

    // Go to 'sent mailbox'
    load_mailbox('sent');
  })

  .catch(error => {
    console.log('Error:', error);
  });
}

// function takes as input an email id, fetches the email by that id
function view_email(email) {
  fetch(`/emails/${email}`)
  .then(response => response.json())
  .then(email => {       

    history.pushState({}, "", `inbox/${email.id}`)
   
    // change innerHTML to reflect that of the email contents
    document.querySelector('#emails-view').innerHTML = `
      <p>from: ${email.sender}<p>
      <p>to: ${email.recipients}</p>      
      <p><strong>${email.subject}</strong></p>    
      <p>${email.timestamp}</p>
      <hr>
      <p>${email.body}</p>`;   

      // archive button
      const archive = document.createElement('button');
      //reply button
      const reply = document.createElement('button');

      archive.textContent = 'Archive mail';  
      archive.id = 'archive_button';
      reply.textContent = 'Reply';
      reply.id = 'reply_button';

      document.querySelector('#emails-view').appendChild(archive);
      document.querySelector('#emails-view').appendChild(reply); 
       
      // upon clicking the archive button, archive the email
      archive.addEventListener('click', () => {
        archive_email(email.id);
        // make sure the inbox is up-to-date before returning to inbox view
        fetch('/emails/inbox')
        .then(() => {
          load_mailbox('inbox');
        })       
      });      
            
      // user clicks reply
      reply.addEventListener('click', () => {

        document.querySelector('#emails-view').style.display = 'none';
        document.querySelector('#compose-view').style.display = 'block';

        history.pushState({}, "", `${email.id}/reply`)

        const recipients = email.sender;
        const subject = `${email.subject}`;
        const body = `\n\n<hr>\n\nOn ${email.timestamp} ${email.sender} wrote: \n${email.body}`;    
              
        
        // variables are prefilled into the reply compose form
        reply_email(recipients, subject, body);                               
      });    
  })  

  // when user views email, set 'read' to true
  fetch(`/emails/${email}`, { 
    method: 'PUT',
    body: JSON.stringify({
        read: true
    })
  })

  .catch(error => {
    console.log('Error:', error);
  });
}

function archive_email(email) {
  fetch(`/emails/${email}`, { 
    method: 'PUT',
    body: JSON.stringify({
        archived: true
    })
  }); 
}

function view_archived_email(email) {
  fetch(`/emails/${email}`)
  .then(response => response.json())
  .then(email => {          

    history.pushState({}, "", `archive/${email.id}`)
    
    document.querySelector('#emails-view').innerHTML = `
      <p>from: ${email.sender}<p>
      <p>to: ${email.recipients}</p>      
      <p><strong>${email.subject}</strong></p>    
      <p>${email.timestamp}</p>
      <p>${email.body}</p>`; 

      // unarchive button
      const unarchive = document.createElement('button');
      unarchive.textContent = 'Unarchive mail';             
      document.querySelector('#emails-view').appendChild(unarchive); 
      
      // upon clicking the button, unarchive the email
      unarchive.addEventListener('click', () => {
        unarchive_email(email.id);
        // make sure the inbox is up-to-date before returning 
        fetch('/emails/inbox')
        .then(() => {
          load_mailbox('inbox');
        })
      }); 
    });   
}

function unarchive_email(email) {
  fetch(`/emails/${email}`, {
    method: 'PUT',
    body: JSON.stringify({
      archived: false
    })
  });
}

function view_sent_email(email) {
  fetch(`/emails/${email}`)
  .then(response => response.json())
  .then(email => {       

    history.pushState({}, "", `sent/${email.id}`)
    
    document.querySelector('#emails-view').innerHTML = `
      <p>from: ${email.sender}<p>
      <p>to: ${email.recipients}</p>      
      <p><strong>${email.subject}</strong></p>    
      <p>${email.timestamp}</p>
      <p>${email.body}</p>`;                  
    });   
}

function reply_email(recipients, subject, body) {
    // Show compose view and hide other views
    document.querySelector('#emails-view').style.display = 'none';
    document.querySelector('#compose-view').style.display = 'block';

    // if subject didn't already start with "Re: ", add it
    if (!subject.startsWith("Re:")) {
      subject = `Re: ${subject}`;
    }   
  
    // fill in fields that need to be pre-filled
    document.querySelector('#compose-recipients').value = recipients;
    document.querySelector('#compose-subject').value = subject;
    document.querySelector('#compose-body').value = body;
}



