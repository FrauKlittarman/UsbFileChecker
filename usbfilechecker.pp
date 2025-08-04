#usbfilechecker
class usbfilechecker {

    $lpu_name = 'LPU_NAME'
    $url = 'https://URL'
    $source_filename = 'FILENAME.xls'
    $target_directory = "/usr/share/usbfilechecker/"


    file { '/var/local/usbfilechecker/':
      ensure  => directory,
      source  => 'puppet:///modules/usbfilechecker/',
      recurse => true,
      owner   => root,
      group   => root,
      mode    => '0644',
      purge   => true,
      force   => true,
    }

    file_line { 'set LPU_NAME':
      ensure  => present,
      path    => '/var/local/usbfilechecker/main.py',
      match   => '^LPU_NAME =',
      line    => "LPU_NAME = \"$lpu_name\""
    }

    file_line { 'set URL':
      ensure  => present,
      path    => '/var/local/usbfilechecker/main.py',
      match   => '^URL =',
      line    => "URL = \"$url\""
    }

    file_line { 'set source filename':
      ensure  => present,
      path    => '/var/local/usbfilechecker/main.py',
      match   => '^SOURCE_FILENAME =',
      line    => "SOURCE_FILENAME = \"$source_filename\""
    }

    file_line { 'set source targert directory':
      ensure  => present,
      path    => '/var/local/usbfilechecker/main.py',
      match   => '^TARGET_DIRECTORY =',
      line    => "TARGET_DIRECTORY = \"$target_directory\""
    }

    cron { 'run usbfileckecher':
      ensure  => present,
      command => "/usr/bin/python3 /var/local/usbfilechecker/main.py",
      user    => root,
      minute  => '*/5'
    }
}
