package main

import (
	"path"
	"path/filepath"
	"os"
	"flag"
	"fmt"
	"bufio"
	//"strings"
	"regexp"
)

func readguid4meta(fpath string) string {
	var line []byte
	//var err error

	fp,_ := os.Open(fpath)
	rdr := bufio.NewReaderSize(fp,100)
	line,_,_ = rdr.ReadLine()
	line,_,_ = rdr.ReadLine()
	defer fp.Close()
	//var s := string(line)
	return string(line)[6:]
}

func pick_guids_file(fpath string ) []string {
	var err error

	re,_ := regexp.Compile("guid: [0-9a-f]{32}")
	res := make([]string,3)

	fp,_ := os.Open(fpath)
	rdr := bufio.NewReaderSize(fp,100)
	for {
		var buf []byte
		buf, _, err = rdr.ReadLine()
		if err != nil {
			break
		}
		///fmt.Printf(string(buf))
		foundx := re.FindAllString(string(buf),9)

		for _, x := range foundx {
			if( x == "00000000000000000000000000000000" || x == "0000000000000000f000000000000000" || x == "0000000000000000e000000000000000" ){
				continue
			}
			res = append(res, x[6:])
		}
		///fmt.Printf("%s\n",found)
		//fmt.Printf(found[0])
	}

	return res
}

var guid_map = make(map[string]string,3)

func register_guid(oname string, guid string ) {
	var ok bool
	if _,ok = guid_map[guid] ; ! ok { // unknown guid
		//fmt.Printf("# %s|.meta: %s\n",oname,guid)
		guid_map[guid] = oname
	} else {
		if guid_map[guid] == oname {

		} else if guid_map[guid][0] != '?' && oname[0] == '?' {

		} else if guid_map[guid][0] == '?' && oname[0] != '?' {
			////fmt.Printf("# %s|.meta: %s\n",oname,guid)
			guid_map[guid] = oname
		} else if guid_map[guid][0] != '?' {
			fmt.Printf("# ? %s!|.meta: %s != %s\n",guid_map[guid],guid,oname )
		} else {
			//fmt.Printf("# %s|.meta: %s\n",oname,guid)
			guid_map[guid] = oname
		}
	}
}

func visit(fpath string, fi os.FileInfo, err error ) error {
	extn := path.Ext(fpath)
	oname := fpath[:len(fpath)-len(extn)]
	switch extn {
	case ".meta":
		guid := readguid4meta(fpath)
		register_guid(oname,guid)
	case ".unity",".mat","prefab","asset":
		///fmt.Printf("? %s\n",fpath )
		ll := pick_guids_file(fpath)
		for _, gs := range ll {
			register_guid("?" + fpath, gs )
		}
		//fmt.Printf("%s\n",ll)
	}
	return nil
}

func main () {
	flag.Parse()
	root := flag.Arg(0)
	filepath.Walk(root,visit)

	for k,v := range guid_map {
		if v[0] == '?' {
			fmt.Printf("%s %s\n",v[1:],k )
		}
	}
}