<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
<meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>شاتي v2</title>
<style>
*{box-sizing:border-box;margin:0;padding:0;font-family:'Segoe UI',Arial}
body{background:#0b141a;height:100vh;display:flex;flex-direction:column}
.header{background:#202c33;color:#fff;padding:12px 15px;display:flex;justify-content:space-between;align-items:center;font-size:18px;font-weight:bold}
.tabs{display:flex;background:#202c33}
.tab{flex:1;text-align:center;padding:12px;color:#aebac1;cursor:pointer;font-weight:500}
.tab.active{border-bottom:3px solid #00a884;color:#fff}
.screen{flex:1;overflow-y:auto;display:none;background:#0b141a}
.screen.active{display:block}
.chat-item{display:flex;align-items:center;padding:12px 15px;background:#111b21;border-bottom:1px solid #202c33;cursor:pointer;color:#fff}
.avatar{width:50px;height:50px;border-radius:50%;margin-left:12px;object-fit:cover}
.chat{padding:10px 15px;padding-bottom:80px}
.msg-row{display:flex;align-items:flex-end;margin:8px 0}
.msg-row.me{justify-content:flex-end}
.avatar-sm{width:35px;height:35px;border-radius:50%;margin-left:8px;object-fit:cover;border:2px solid #00a884}
.msg{background:#202c33;color:#e9edef;padding:10px 14px;border-radius:8px;max-width:75%}
.msg.me{background:#005c4b}
.sender{font-size:13px;font-weight:700;color:#00a884}
.number{font-size:11px;color:#8696a0;margin-bottom:4px}
.msg img{max-width:240px;border-radius:8px;margin-top:5px;display:block}
.footer{font-size:11px;color:#8696a0;text-align:right;margin-top:4px}
.input-area{display:flex;position:fixed;bottom:0;width:100%;background:#202c33;padding:8px;gap:5px}
.input-area input{flex:1;padding:12px 15px;border:none;border-radius:25px;background:#2a3942;color:#fff;font-size:15px}
.input-area button{background:#00a884;color:#fff;border:none;width:45px;height:45px;border-radius:50%;font-size:20px;cursor:pointer}
#loginScreen{text-align:center;background:#111b21;color:#fff;height:100vh;padding-top:50px}
#loginScreen input{width:80%;padding:12px;margin:10px 0;border:1px solid #2a3942;border-radius:8px;font-size:15px;background:#2a3942;color:#fff}
#loginScreen button{background:#00a884;color:#fff;border:none;padding:12px 30px;border-radius:8px;font-size:16px;cursor:pointer}
</style>
</head>
<body>
  <div class="header"><div id="appTitle">شاتي v2</div><span onclick="addContact()" style="font-size:24px;cursor:pointer">+</span></div>
  <div class="tabs" id="tabs" style="display:none">
    <div class="tab active" onclick="showTab('chatListScreen')">الدردشات</div>
    <div class="tab" onclick="showTab('statusScreen')">الحالة</div>
  </div>

  <div id="loginScreen" class="screen active">
    <h2>مرحبا في <span style="color:#00a884">شاتي v2</span></h2>
    <input type="text" id="myNameInput" placeholder="اكتب اسمك هنا" required><br>
    <input type="tel" id="myNumberInput" placeholder="اكتب رقمك هنا" required><br>
    <button onclick="saveProfile()">بدء الدردشة</button>
  </div>

  <div id="chatListScreen" class="screen">
    <div class="chat-item" onclick="openChat('عام')">
      <img class="avatar" src="https://i.imgur.com/8Km9tLL.png">
      <div><b>المجموعة العامة</b></div>
    </div>
    <div id="contactsList"></div>
  </div>

  <div id="chatScreen" class="screen">
    <div class="chat" id="chat"></div>
    <div class="input-area">
      <label for="fileInput" style="background:#00a884;color:#fff;width:45px;height:45px;border-radius:50%;display:flex;align-items:center;justify-content:center;font-size:20px;cursor:pointer">📎</label>
      <input type="file" id="fileInput" accept="image/*" style="display:none">
      <button onclick="sendMsg()">➤</button>
      <input type="text" id="msgInput" placeholder="اكتب رسالة" onkeypress="if(event.key==='Enter')sendMsg()">
    </div>
  </div>

<script src="https://www.gstatic.com/firebasejs/8.10.1/firebase-app.js"></script>
<script src="https://www.gstatic.com/firebasejs/8.10.1/firebase-database.js"></script>
<script>
const firebaseConfig = {
  apiKey: "AIzaSyASYXDPEaYDovYuU_gd83734aJ_nofvKrQ",
  authDomain: "project-name-5ce26.firebaseapp.com",
  databaseURL: "https://project-name-5ce26-default-rtdb.asia-southeast1.firebasedatabase.app",
  projectId: "project-name-5ce26"
};
firebase.initializeApp(firebaseConfig);
const db = firebase.database();
localStorage.clear(); // نمسح اي بيانات قديمة اجباري

let profile = {};
let contacts = JSON.parse(localStorage.getItem('contacts_v2')) || [];
let currentChat = 'عام';
const IMGBB_KEY = '6b8bfa5617ae2be9c6c5e1e9b5e5e5e5';

function showApp(){
  document.getElementById('loginScreen').classList.remove('active');
  document.getElementById('tabs').style.display='flex';
  document.getElementById('chatListScreen').classList.add('active');
  document.getElementById('appTitle').innerText = profile.name;
  loadContacts(); listenMessages();
}

function saveProfile(){
  let name = document.getElementById('myNameInput').value;
  let number = document.getElementById('myNumberInput').value;
  if(name=="" || number==""){alert("لازم تكتب الاسم والرقم");return;}
  profile = {name, number, avatar:"https://i.pravatar.cc/150?u="+number};
  localStorage.setItem('profile_v2', JSON.stringify(profile));
  showApp();
}

function showTab(id){
  document.querySelectorAll('.screen').forEach(s=>s.classList.remove('active'));
  document.getElementById(id).classList.add('active');
  document.querySelectorAll('.tab').forEach(t=>t.classList.remove('active'));
  event.target.classList.add('active');
}

function addContact(){let name = prompt("اسم الشخص:");if(name){contacts.push({name});localStorage.setItem('contacts_v2',JSON.stringify(contacts));loadContacts();}}
function loadContacts(){document.getElementById('contactsList').innerHTML='';contacts.forEach(c=>{document.getElementById('contactsList').innerHTML+=`<div class="chat-item" onclick="openChat('${c.name}')"><img class="avatar" src="https://i.pravatar.cc/150?u=${c.name}"><div><b>${c.name}</b></div></div>`})}
function openChat(p){currentChat = p;document.getElementById('chatListScreen').classList.remove('active');document.getElementById('chatScreen').classList.add('active');document.getElementById('appTitle').innerText = p;document.getElementById('chat').innerHTML='';listenMessages();}

function showMsg(msg){
  let from = msg.from || "مجهول";
  let number = msg.number || "";
  let avatar = msg.avatar || "https://i.pravatar.cc/150?u=guest";
  const isMe = from === profile.name;
  const show = currentChat==='عام'? true : (msg.to===profile.name || from===profile.name);
  if(!show) return;
  let content = msg.text || '';
  if(msg.image) content = `<img src="${msg.image}">` + content;

  document.getElementById('chat').innerHTML += `<div class="msg-row ${isMe?'me':''}">
    ${!isMe?`<img class="avatar-sm" src="${avatar}">`:''}
    <div class="msg ${isMe?'me':''}">
      ${!isMe?`<div class="sender">${from}</div><div class="number">${number}</div>`:''}
      ${content}
      <div class="footer">${msg.time} ${isMe?'✓✓':''}</div>
    </div>
  </div>`;
  document.getElementById('chat').scrollTop = document.getElementById('chat').scrollHeight;
}

function listenMessages(){db.ref('messages').on('child_added', (data)=>{showMsg(data.val());});}

function sendMsg(){
  let input = document.getElementById('msgInput');
  if(input.value.trim()!= ""){
    db.ref('messages').push({from:profile.name,to:currentChat,text:input.value,number:profile.number,avatar:profile.avatar,time:new Date().toLocaleTimeString('ar-EG',{hour:'2-digit',minute:'2-digit'})});
    input.value = "";
  }
}

document.getElementById('fileInput').onchange = function(e){
  let file = e.target.files[0]; if(!file) return;
  let form = new FormData();
  form.append('image', file);
  form.append('key', IMGBB_KEY);
  fetch('https://api.imgbb.com/1/upload', {method:'POST', body:form})
.then(res => res.json())
.then(data => {
    if(data.success){
      let url = data.data.url;
      db.ref('messages').push({from:profile.name,to:currentChat,image:url,text:'',number:profile.number,avatar:profile.avatar,time:new Date().toLocaleTimeString('ar-EG',{hour:'2-digit',minute:'2-digit'})});
    }else{alert("فشل رفع الصورة")}
  }).catch(err=>alert("تأكد من النت"));
}
</script>
</body></html> 
