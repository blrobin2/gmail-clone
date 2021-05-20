<template>
  <div class="bulk-action-bar">
    <span>
      <input
        id="select-all-emails"
        name="select-all-emails"
        type="checkbox"
        :checked="allEmailsSelected"
        :indeterminate="someEmailsSelected"
        class="form-check-input"
        @click="bulkSelect"
      />
      <label class="visually-hidden" for="select-all-emails">Select All</label>
    </span>
    &nbsp;
    <span class="btn-group" role="button" aria-label="Bulk Actions">
      <button
        class="btn btn-sm btn-outline-secondary"
        @click="emailSelection.markRead"
        :disabled="[...emailSelection.emails].every(e => e.read)"
      >
        Mark Read
      </button>
      <button
        class="btn btn-sm btn-outline-secondary"
        @click="emailSelection.markUnread"
        :disabled="[...emailSelection.emails].every(e => !e.read)"
      >
        Mark Unread
      </button>
      <button
        class="btn btn-sm btn-outline-secondary"
        @click="emailSelection.archive"
        :disabled="numberSelected === 0"
      >
        Archive
      </button>
    </span>
  </div>
</template>

<script>
import { computed } from 'vue';

import useEmailSelection from '@/composables/use-email-selection';

export default {
  setup(props) {
    const emailSelection = useEmailSelection();
    const numberSelected = computed(() => emailSelection.emails.size);
    const numberEmails = computed(() => props.emails.length);
    const allEmailsSelected = computed(() => numberSelected.value === numberEmails.value && numberEmails.value > 0);
    const someEmailsSelected = computed(() => {
      return numberSelected.value > 0 && numberSelected.value < numberEmails.value;
    });

    const bulkSelect = () => {
      if (allEmailsSelected.value) {
        emailSelection.clear();
      } else {
        emailSelection.addMultiple(props.emails);
      }
    };

    return {
      allEmailsSelected,
      someEmailsSelected,
      bulkSelect,
      emailSelection,
      numberSelected,
    };
  },
  props: {
    emails: {
      type: Array,
      required: true,
    },
  },
};
</script>
