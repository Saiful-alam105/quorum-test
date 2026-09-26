/**
 * User directory rendering helpers.
 *
 * This file contains a non-Python (JavaScript) demo so that Quorum can
 * demonstrate language/file handling for files that are not Python.
 */

const userListElement = document.getElementById('user-list');

/**
 * Format a user object into a plain text summary.
 * @param {Object} user
 * @returns {string}
 */
function formatUser(user) {
  const name = user.name || 'Unknown';
  const role = user.role || 'member';
  const online = user.online ? 'online' : 'offline';
  return `${name} (${role}) - ${online}`;
}

/**
 * Build an HTML string for a single user card.
 * @param {Object} user
 * @returns {string}
 */
function buildUserCard(user) {
  const avatar = user.avatarUrl || 'https://example.com/default-avatar.png';
  const badge = user.admin ? '<span class="badge">admin</span>' : '';
  return `
    <div class="user-card" data-id="${user.id}">
      <img src="${avatar}" alt="${escapeHtml(user.name || '')}" />
      <h3>${escapeHtml(user.name || '')}</h3>
      <p>${escapeHtml(user.email || '')}</p>
      ${badge}
    </div>
  `;
}

/**
 * Escape a string for safe insertion into HTML.
 * @param {string} value
 * @returns {string}
 */
function escapeHtml(value) {
  return String(value)
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;')
    .replace(/'/g, '&#39;');
}

/**
 * Render a single user card and return its element.
 * @param {Object} user
 * @returns {HTMLElement}
 */
function renderUser(user) {
  const container = document.createElement('div');
  container.innerHTML = buildUserCard(user);
  return container.firstElementChild;
}

/**
 * Render a user's profile summary into a target element.
 * @param {Object} user
 * @param {HTMLElement} target
 */
function renderProfile(user, target) {
  const card = renderUser(user);
  const meta = document.createElement('p');
  meta.className = 'profile-meta';
  meta.textContent = formatUser(user);
  card.appendChild(meta);
  target.appendChild(card);
  return card;
}

/**
 * Update the user list UI with a set of users.
 * @param {Array<Object>} users
 */
function updateUserList(users) {
  if (!userListElement) {
    return;
  }
  userListElement.innerHTML = '';
  users.forEach((user) => {
    userListElement.appendChild(renderUser(user));
  });
}

/**
 * Sort users by name and render them.
 * @param {Array<Object>} users
 * @param {HTMLElement} target
 */
function renderSortedUsers(users, target) {
  const sorted = users.slice().sort((a, b) => {
    const nameA = (a.name || '').toLowerCase();
    const nameB = (b.name || '').toLowerCase();
    return nameA.localeCompare(nameB);
  });
  sorted.forEach((user) => renderProfile(user, target));
}

/**
 * Filter users to online members only.
 * @param {Array<Object>} users
 * @returns {Array<Object>}
 */
function onlineMembers(users) {
  return users.filter((user) => user.online && user.role === 'member');
}

if (typeof module !== 'undefined' && module.exports) {
  module.exports = {
    formatUser,
    buildUserCard,
    escapeHtml,
    renderUser,
    renderProfile,
    updateUserList,
    renderSortedUsers,
    onlineMembers
  };
}