{pkgs}: {
  deps = [
    pkgs.gnupg1orig
    pkgs.unixODBC
    pkgs.cacert
    pkgs.glibcLocales
    pkgs.unixODBCDrivers.msodbcsql17
  ];
}