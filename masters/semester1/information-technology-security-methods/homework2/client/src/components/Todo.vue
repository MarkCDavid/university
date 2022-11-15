<template>
  <div>
    <input
      type="checkbox"
      :id="todo"
      :checked="isChecked"
      @change="$emit('toggled', todo.id)"
    />
    <label :class="{ finished: todo.completed }" :for="todo">
      {{ todo.value }}
    </label>
    <button @click="$emit('deleted', todo.id)">X</button>
  </div>
</template>

<script>
import { ref } from "@vue/reactivity";
export default {
  name: "Todo",
  emits: ["toggled", "deleted"],
  props: {
    certificate: String,
    todo: Object,
  },
  setup(props) {
    const isChecked = ref(props.todo.completed);

    return { isChecked };
  },
};
</script>

<style scoped>
.finished {
  text-decoration: line-through;
}
</style>