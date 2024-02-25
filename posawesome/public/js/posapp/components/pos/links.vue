<template>
    <v-main>
      <div class="links-container">
        <div
          v-for="(link, index) in links"
          :key="index"
          class="link-card"
          @click="navigateTo(link.url)"
        >
          <div class="link-card-content">
            <v-icon class="link-icon">{{ link.icon }}</v-icon>
            <h3 class="link-title">{{ link.title }}</h3>
          </div>
        </div>
      </div>
    </v-main>
  </template>
  
  <script>
  export default {
    data() {
      return {
        links: [
          { title: __('Payment Entry'), url: frappe.urllib.get_base_url() + '/app/payment-entry/new', icon: 'mdi-cash' },
          { title: __('All Payment Entries'), url: frappe.urllib.get_base_url() + '/app/payment-entry', icon: 'mdi-cash-multiple' },
          { title: __('Sales Invoice'), url: frappe.urllib.get_base_url() + '/app/sales-invoice', icon: 'mdi-file-send' },
          { title: __('General Ledger'), url: frappe.urllib.get_base_url() + '/app/query-report/General Ledger', icon: 'mdi-chart-line' },
          { title: __('Customer Ledger Summery'), url: frappe.urllib.get_base_url() + '/app/query-report/Customer Ledger Summary', icon: 'mdi-chart-pie' },
          { title: __('Expense Entry'), url: frappe.urllib.get_base_url() + '/app/expense-entry/new', icon: 'mdi-cash-plus' },
        ]
      };
    },
    methods: {
      navigateTo(url) {
        // If the URL is a relative path, navigate using Vue Router
        if (url.startsWith('/')) {
          this.$router.push(url);
        } else {
          // Open external links in a new tab
          window.open(url, '_blank');
        }
      }
    }
  };
  </script>
  
  <style scoped>
  .links-container {
    display: flex;
    flex-wrap: wrap;
    justify-content: flex-start;
    align-items: flex-start;
    padding: 20px; /* Add some padding for spacing */
  }
  
  .link-card {
    width: 200px; /* Adjust as needed */
    height: 200px; /* Same as width for a square */
    margin: 10px; /* Adjust spacing between cards */
    border-radius: 10px; /* Rounded corners */
    display: flex;
    justify-content: center;
    align-items: center;
    text-align: center;
    cursor: pointer;
  }
  
  .link-card:hover {
    box-shadow: 0 0 10px rgba(0, 0, 0, 0.1); /* Add shadow on hover */
  }
  
  .link-card-content {
    display: flex;
    flex-direction: column;
    align-items: center;
  }
  
  .link-icon {
    font-size: 48px; /* Adjust icon size */
  }
  
  .link-title {
    margin: 10px 0 0; /* Add margin to separate icon and title */
  }
  </style>
  