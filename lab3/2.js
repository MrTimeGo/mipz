/*
Запахи коду:
- Роздувальщик - Групи даних


Методи рефакторингу:
- Створення ієрархії класів з полями і методами, що використовуються у всіх типах користувачів
*/

class User {
  constructor(name, email, role) {
    this.name = name;
    this.email = email;
    this.role = role;
  }

  login() {
    const capitalizedRole =
      this.role.charAt(0).toUpperCase() + this.role.slice(1);
    console.log(`${capitalizedRole} ${this.name} logged in.`);
  }
  logout() {
    const capitalizedRole =
      this.role.charAt(0).toUpperCase() + this.role.slice(1);
    console.log(`${capitalizedRole} ${this.name} logged out.`);
  }
}

class Admin extends User {
  constructor(name, email) {
    super(name, email, "admin");
  }

  accessDashboard() {
    console.log("Admin dashboard accessed by " + this.name);
  }
}

class Editor extends User {
  constructor(name, email) {
    super(name, email, "editor");
  }

  editContent() {
    console.log("Editor " + this.name + " is editing content.");
  }
}

class Viewer extends User {
  constructor(name, email) {
    super(name, email, "viewer");
  }

  viewContent() {
    console.log("Viewer " + this.name + " is viewing content.");
  }
}

// Usage
const admin = new Admin("Alice", "alice@example.com");
admin.login();
admin.accessDashboard();
admin.logout();
const editor = new Editor("Bob", "bob@example.com");
editor.login();
editor.editContent();
editor.logout();
const viewer = new Viewer("Charlie", "charlie@example.com");
viewer.login();
viewer.viewContent();
viewer.logout();
