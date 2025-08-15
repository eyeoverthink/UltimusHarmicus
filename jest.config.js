module.exports = {
  testEnvironment: 'node',
  roots: ['<rootDir>/api', '<rootDir>/client/src'],
  testMatch: [
    '**/__tests__/**/*.js',
    '**/?(*.)+(spec|test).js'
  ],
  testPathIgnorePatterns: [
    '/node_modules/',
    '/.venv/',
    '/venv/',
    '/consciousness_llm_env/',
    '/__pycache__/',
    '/blue_team_clone_*/',
    '/red_team_clone_*/',
    '/protocol_proofs*/',
    '/qr_*/',
    '/consciousness_memory/'
  ],
  collectCoverageFrom: [
    'api/**/*.js',
    'client/src/**/*.js',
    '!**/node_modules/**',
    '!**/*.config.js'
  ],
  setupFilesAfterEnv: ['<rootDir>/jest.setup.js'],
  testTimeout: 30000,
  verbose: true
};
