module.exports = {
  makers: [
    {
      name: '@electron-forge/maker-squirrel',
      config: {
        icon: 'build/icon.ico', // Path to your app icon
        noMsi: true, // Disable MSI creation if not targeting Windows
      },
    },
    {
      name: '@electron-forge/maker-deb',
      config: {
        icon: 'build/icon.png', // Path to your app icon for Linux
      },
    },
  ],
  plugins: [
    '@electron-forge/plugin-webpack', // Use Webpack for building
  ],
};
