const form = document.querySelector("#signup-form");

const checkPassword = () => {
  const formData = new FormData(form);
  const password1 = formData.get("password");
  const password2 = formData.get("password2");

  if (password1 === password2) {
    return true;
  } else return false;
};

const handleSubmit = async (event) => {
  event.preventDefault();
  const formData = new FormData(form); //id password 값 들어옴
  const sha256Password = CryptoJS.SHA256(formData.get("password")).toString(); // sha256으로 암호화

  formData.set("password", sha256Password); // 그걸 다시 formData에 넣어줌
  console.log(formData.get("password"));

  const div = document.querySelector("#info");

  if (checkPassword()) {
    const res = await fetch("/signup", {
      method: "post",
      body: formData,
    });
    const data = await res.json();

    if (data === "200") {
      // div.innerText = "회원가입에 성공했습니다";
      alert("회원 가입에 성공했습니다.");
      window.location.pathname = "/login.html";
    }
  } else {
    div.innerText = "비밀번호가 같지 않습니다.";
  }
};

form.addEventListener("submit", handleSubmit);
