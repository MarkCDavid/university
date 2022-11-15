<template>
  <div>
    <!-- LOGIN -->
    <div v-if="certificate == null">
      <input type="file" @change="previewFiles" single />
    </div>
    <!-- LOGGED IN -->
    <div v-if="certificate != null">
      <button @click="logOut">Log out</button>
      <div>
        <input v-model="todoText" type="text" placeholder="Todo..." />
        <button @click="addNew">Add new</button>
      </div>
      <Todo
        @toggled="onChange"
        @deleted="onDelete"
        :certificate="certificate"
        :todo="todo"
        v-for="todo in todos"
        v-bind:key="todo.id"
      ></Todo>
    </div>
  </div>
</template>

<script>
import Todo from "./components/Todo.vue";
import { ref } from "vue";

export default {
  components: {
    Todo,
  },
  setup() {
    const certificate = ref(null);
    const todoText = ref("");
    const todos = ref([]);

    const previewFiles = (event) => {
      const file = event.target.files[0];
      const reader = new FileReader();
      reader.onload = async (event) => {
        certificate.value = event.target.result;
        await refresh();
      };
      reader.onerror = (event) => console.log(event);
      reader.readAsText(file);
    };

    const logOut = () => {
      certificate.value = null;
    };

    const refresh = async () => {
      var response = await fetch("https://server.itsm.local:8006/all", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          certificate: certificate.value,
        }),
      });

      var data = await response.json();
      todos.value = data.todos;
    };

    const addNew = async () => {
      if (todoText.value.length > 0) {
        await fetch("https://server.itsm.local:8006/add", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            certificate: certificate.value,
            value: todoText.value,
          }),
        });
        todoText.value = "";
        await refresh();
      }
    };

    const onChange = async (id) => {
      await fetch("https://server.itsm.local:8006/toggle", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          certificate: certificate.value,
          id: id,
        }),
      });
      await refresh();
    };

    const onDelete = async (id) => {
      await fetch("https://server.itsm.local:8006/delete", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          certificate: certificate.value,
          id: id,
        }),
      });
      await refresh();
    };

    return {
      onChange,
      onDelete,
      todos,
      todoText,
      addNew,
      logOut,
      certificate,
      previewFiles,
    };
  },
};
</script>

<style>
</style>
