// Sample Cypress test (requires configuring baseUrl)
// Put this into cypress/e2e/sample_spec.cy.js when Cypress is set up

describe('Hotel demo flow', () => {
  it('loads homepage', () => {
    cy.visit('/')
    cy.contains('Hotel Management - Demo')
  })
})
