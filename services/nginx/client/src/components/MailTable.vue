<template>
  <div class="btn-group float-end" role="button" aria-label="Toggle Inbox and Archive">
    <button
      class="btn btn-lg btn-outline-primary"
      @click="selectScreen('inbox')"
      :disabled="selectedScreen === 'inbox'"
    >
      Inbox
    </button>
    <button
      class="btn btn-lg btn-outline-primary"
      @click="selectScreen('archive')"
      :disabled="selectedScreen === 'archive'"
    >
      Archive
    </button>
  </div>
  <table class="table mail-table">
    <tbody>
      <tr>
        <td colspan="5">
          <bulk-action-bar :emails="filteredEmails" />
        </td>
      </tr>
      <tr v-for="email in filteredEmails"
        :key="email.id"
        :class="[email.read ? 'read' : '', emailSelection.emails.has(email) ? 'table-primary' : '']"
      >
        <td scope="row">
          <input type="checkbox"
            @click="emailSelection.toggle(email)"
            :checked="emailSelection.emails.has(email)"
            class="form-check-input"
          />
        </td>
        <td>{{ email.from_email }}</td>
        <td class="clickable" @click="openEmail(email)">
          <p><strong>{{ subjectSubstring(email) }}</strong> - {{ bodySubstring(email) }}</p>
        </td>
        <td class="clickable date" @click="openEmail(email)">
          {{ format(new Date(email.sent_at), 'MMMM do yyyy') }}
        </td>
        <td v-if="onInboxScreen">
          <button class="btn btn-sm btn-info" @click="markEmailArchived(email)">Archive</button>
        </td>
        <td v-if="onArchiveScreen">
          <button class="btn btn-sm btn-info" @click="markEmailUnarchived(email)">Inbox</button>
        </td>
      </tr>
    </tbody>
  </table>
  <modal-view @closeModal="closeEmail" :ref="setModal" v-if="openedEmail">
    <template v-slot:header>
      <h2 class="mb-0">Subject: <strong>{{ openedEmail.subject }}</strong></h2>
    </template>
    <template v-slot:default>
      <mail-view :email="openedEmail" @changeEmail="changeEmail" />
    </template>
  </modal-view>
</template>

<script>
import { Modal } from 'bootstrap';
import { format } from 'date-fns';
import { ref } from 'vue';

import { getEmails, updateEmail } from '@/services/emailService';
import useEmailSelection from '@/composables/use-email-selection';
import BulkActionBar from '@/components/BulkActionBar.vue';
import MailView from '@/components/MailView.vue';
import ModalView from '@/components/ModalView.vue';

const SUBJECT_MAX_LENGTH = 90;
const BODY_MAX_LENGTH = 100;

export default {
  async setup() {
    let modal = null;
    const setModal = el => {
      if (el) {
        modal = new Modal(el.$el);
        modal.show();
      }
    };
    const closeModal = () => {
      modal.hide();
      modal = null;
    };

    const emails = await getEmails();
    return {
      emailSelection: useEmailSelection(),
      format,
      setModal,
      closeModal,
      "emails": ref(emails),
      openedEmail: ref(null),
      selectedScreen: ref('inbox'),
    };
  },
  components: {
    BulkActionBar,
    MailView,
    ModalView,
  },
  methods: {
    selectScreen(newScreen) {
      this.selectedScreen = newScreen;
      this.emailSelection.clear();
    },
    subjectSubstring(email) {
      const subject = email.subject.substring(0, SUBJECT_MAX_LENGTH);
      if (subject.length < email.subject.length) {
        return subject + "\u2026";
      }
      return subject;
    },
    bodySubstring(email) {
      if (this.subjectSubstring(email).length >= SUBJECT_MAX_LENGTH) {
        return '';
      }
      const body = email.body.substring(0, BODY_MAX_LENGTH - email.subject.length);
      if (body.length < email.body.length) {
        return body + "\u2026";
      }
      return body;
    },
    openEmail(email) {
      email.read = true;
      this.updateEmail(email);
      this.openedEmail = email;
    },
    closeEmail() {
      this.closeModal();
      this.openedEmail = null;
    },
    markEmailArchived(email) {
      email.archived = true;
      this.updateEmail(email);
    },
    markEmailUnarchived(email) {
      email.archived = false;
      this.updateEmail(email);
    },
    changeEmail({
      toggleRead,
      toggleArchive,
      save,
      closeModal,
      changeIndex
    }) {
      const email = this.openedEmail;
      if (toggleRead) { email.read = !email.read; }
      if (toggleArchive) { email.archived = !email.archived; }
      if (save) { this.updateEmail(email); }
      if (changeIndex) {
        const emails = this.filteredEmails;
        const currentIndex = emails.indexOf(this.openedEmail);
        let newIndex = currentIndex + changeIndex;
        if (newIndex > emails.length - 1) {
          newIndex = 0;
        }
        if (newIndex < 0) {
          newIndex = emails.length - 1;
        }
        const newEmail = emails[newIndex];
        this.openEmail(newEmail);
      }
      if (closeModal) {
        this.closeEmail();
      }
    },
    updateEmail(email) {
      updateEmail(email.id, email).catch(err => {
        console.error(err);
      });
    },
  },
  computed: {
    filteredEmails() {
      if (this.selectedScreen === 'inbox') {
        return this.unarchivedEmails;
      }
      return this.archivedEmails;
    },
    unarchivedEmails() {
      return this.emails.filter(e => !e.archived);
    },
    archivedEmails() {
      return this.emails.filter(e => e.archived);
    },
    onInboxScreen() {
      return this.selectedScreen === 'inbox';
    },
    onArchiveScreen() {
      return this.selectedScreen === 'archive';
    }
  }
};
</script>

<style scoped>
  .clickable {
    cursor: pointer;
  }
  .read {
    opacity: 0.5;
  }
</style>
