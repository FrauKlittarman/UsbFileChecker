#usbfilechecker
class usbfilechecker (
  String $source_filename = 'test.xls',
  String $minute = '*/10',
  Array[String] $hours = ['7-19'],
){
    ensure_packages ( ['python3-toml',] )

    file { '/var/local/usbfilechecker/':
      ensure  => directory,
      source  => 'puppet:///modules/usbfilechecker/',
      recurse => true,
      owner   => root,
      group   => root,
      mode    => '0750',
      purge   => true,
      force   => true,
      ignore  => ['__pycache__', 'pyproject.toml'],
    }

    file { '/var/local/usbfilechecker/pyproject.toml':
      ensure  => directory,
      source  => 'puppet:///modules/usbfilechecker/pyproject.toml',
      owner   => root,
      group   => root,
      mode    => '0640',
      replace => false,
    }

    file_line { 'set source filename':
      ensure  => present,
      path    => '/var/local/usbfilechecker/pyproject.toml',
      match   => '^filename=',
      line    => "filename=\"${source_filename}\""
    }

    cron { 'run usbfilechecker':
      ensure  => present,
      command => "/usr/bin/python3 /var/local/usbfilechecker/main.py > /dev/null 2>&1",
      user    => root,
      hour    => $hours,
      minute  => $minute,
    }
}
