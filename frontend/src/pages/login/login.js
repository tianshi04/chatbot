// document.getElementById("login-btn").addEventListener("click", function() {
//     const popupWidth = 550
//     const popupHeight = 650

//     const left = (window.screen.width / 2) - (popupWidth / 2)
//     const top = (window.screen.height / 2) - (popupHeight / 2)

//     window.open(
//         "/auth/login",
//         "googleLoginPopup",
//         `width=${popupWidth},height=${popupHeight},left=${left},top=${top}`
//     )
// })

function handleCredentialResponse(response) {
    const token = response.credential;

    fetch('/auth/callback', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ token }),
    })
    .then(response => {
        if (response.ok) {
            window.location.href = '/home';
        } else {
            console.error('Login failed');
        }
    })
    .catch(error => {
        console.error('Error:', error);
    });
}

window.onload = function () {
    google.accounts.id.initialize({
        client_id: '107320473100-k58pa5bs0d29nu6gno263bjpv4utr0ij.apps.googleusercontent.com',
        callback: handleCredentialResponse
    });
    
    google.accounts.id.renderButton(
        document.querySelector('.g_id_signin'),
        { theme: 'outline', size: 'large' }
    );
    
    google.accounts.id.prompt();
};
