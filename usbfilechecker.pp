#usbfilechecker
class usbfilechecker (
  String $source_filename = 'FILENAME.xls',
  Array[String] $packages = ['python3‑toml'],
  String $minute = '*/5',
){

    ensure_resources('package', { $packages => {} }, { 'ensure' => 'present' })

    file { '/var/local/usbfilechecker/':
      ensure  => directory,
      source  => 'puppet:///modules/usbfilechecker/',
      recurse => true,
      owner   => root,
      group   => root,
      mode    => '0750',
      purge   => true,
      force   => true,
    }

    file_line { 'set source filename':
      ensure  => present,
      path    => '/var/local/usbfilechecker/pyproject.toml',
      match   => '^filename =',
      line    => "filename = \"${source_filename}\""
    }

    cron { 'run usbfilechecker':
      ensure  => present,
      command => "/usr/bin/python3 /var/local/usbfilechecker/main.py > /dev/null 2>&1",
      user    => root,
      minute  => $minute,
    }
}
