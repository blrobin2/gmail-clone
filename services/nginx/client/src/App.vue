<template>
  <div class="container">
    <h1>Inbox</h1>
    <h3>{{ emailSelection.emails.size }} emails selected</h3>

    <Suspense>
      <template #default>
        <MailTable />
      </template>
      <template #fallback>
        Loading&hellip;
      </template>
    </Suspense>
  </div>
</template>

<script>
  import MailTable from '@/components/MailTable.vue';
  import useEmailSelection from '@/composables/use-email-selection';

  export default {
    name: 'App',
    components: {
      MailTable
    },
    setup() {
      return {
        emailSelection: useEmailSelection(),
      };
    },
  };
</script>
