const form = document.querySelector("#login-form");

const handleSubmit = async (event) => {
  event.preventDefault();
  const formData = new FormData(form); //id password 값 들어옴
  const sha256Password = CryptoJS.SHA256(formData.get("password")).toString(); // sha256으로 암호화

  formData.set("password", sha256Password); // 그걸 다시 formData에 넣어줌

  console.log(formData.get("password"));

  const res = await fetch("/login", {
    method: "POST",
    body: formData,
  });
  const data = await res.json();
  const accessToken = data.access_token;
  window.localStorage.setItem("token", accessToken); // 창을 닫았다 열어도 로그인정보 저장
  //   window.sessionStorage.setItem("token", accessToken);// 창을 닫았다 열면 로그인 정보 삭제
  //   console.log(accessToken);
  alert("로그인 되었습니다.");
  window.location.pathname = "/";
};

form.addEventListener("submit", handleSubmit);
