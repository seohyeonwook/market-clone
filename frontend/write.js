const form = document.getElementById("write-form");

const handleSubmitForm = async (event) => {
  event.preventDefault(); // submit console창에서 초기화 되는거 막기 위해서
  console.log("제출"); // submit잘 되는지 확인하기위해서
  try {
    const res = await fetch("/items", {
      method: "POST",
      body: new FormData(form),
    });
    console.log("제출완료");
    const data = await res.json();
    if (data === "200") window.location.pathname = "/";
  } catch (e) {
    console.error(e);
  }

  // 이렇게 서버로 보낸다 그다음에 터미널창에
  // UploadFile(filename='', size=0, headers=Headers({'content-disposition': 'form-data; name="image"; filename=""', 'content-type': 'application/octet-stream'})) ㄴㅇㄹㄴ 12 ㅇㄴㄹ ㄴㅇㄹ
  // INFO:     127.0.0.1:4204 - "POST /items HTTP/1.1" 200 OK
  // 대충 이렇게 뜨면 된다
};
form.addEventListener("submit", handleSubmitForm);
