#usbfilechecker
class usbfilechecker {
    
    $LPU_NAME   = '<LPU_NAME>'
    $URL    = 'https://URL'
    $SOURCE_FILENAME = 'filename.xls'


    file { '/var/local/usb_file_checker/':
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
      line    => "LPU_NAME = \"$LPU_NAME\""
    }

    file_line { 'set URL':
      ensure  => present,
      path    => '/var/local/usbfilechecker/main.py',
      match   => '^URL =',
      line    => "URL = \"$URL\""
    }

    file_line { 'set source filename':
      ensure  => present,
      path    => '/var/local/usbfilechecker/main.py',
      match   => '^SOURCE_FILENAME =',
      line    => "SOURCE_FILENAME = \"$SOURCE_FILENAME\""
    }

    cron {'run usbfileckecher':
      ensure  => present,
      command => "/usr/bin/python3 /var/local/usbfilechecker/main.py",
      user    => root,
      minute  => '*/5'
    }
}
